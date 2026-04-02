"""
interactive.py - Full Interactive Mode
คำสั่งครบ: /use /all /run /compare /consensus
"""
import sys
import os
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import Orchestrator, C, color_for, print_result, print_results, print_summary, LINE
from skills_registry import SkillsRegistry, Strategy
from utils import print_header


class InteractiveCLI:
    def __init__(self):
        self.orch = Orchestrator()
        self.skills = SkillsRegistry()
        self.active_agents: list = []     # ว่าง = ไม่ได้เลือก
        self.all_agent_ids = list(self.orch.agents_cfg.keys())
        self.enabled_ids = list(self.orch.get_enabled_agents().keys())

    # ─── Header ───────────────────────────────────────────────────────────────
    def _header(self):
        print_header()
        
        enabled = [a.upper() for a in self.enabled_ids]
        print(f" {C.DIM}● Ready Agents: {', '.join(enabled)}{C.RESET}\n")
        self._show_active()

    def _show_active(self):
        if not self.active_agents:
            print(f"  {C.YELLOW}📌 Active: [Auto Mode] — ระบบจะเลือก AI ให้เอง{C.RESET}\n")
        else:
            names = ", ".join(a.upper() for a in self.active_agents)
            print(f"  {C.GREEN}📌 Active: {names}{C.RESET}\n")


    def _prompt_prefix(self) -> str:
        if not self.active_agents:
            return f"{C.DIM}[no agents]{C.RESET}"
        if len(self.active_agents) == len(self.all_agent_ids):
            return f"{C.CYAN}[all]{C.RESET}"
        names = ",".join(self.active_agents)
        return f"{C.GREEN}[{names}]{C.RESET}"

    # ─── Commands ─────────────────────────────────────────────────────────────
    def cmd_use(self, args: str):
        """  /use qwen  หรือ  /use codex,qwen"""
        if not args:
            print(f"  {C.YELLOW}การใช้งาน: /use <agent> หรือ /use <a1>,<a2>{C.RESET}")
            return

        requested = [a.strip().lower() for a in args.split(",")]
        selected = []
        for aid in requested:
            if aid not in self.orch.agents_cfg:
                print(f"  {C.RED}ไม่รู้จัก '{aid}'{C.RESET}")
                continue
            if not self.orch.agents_cfg[aid].get("enabled", False):
                print(f"  {C.YELLOW}⚠️  {aid} ปิดอยู่ (enabled: false){C.RESET}")
                continue
            selected.append(aid)

        if selected:
            self.active_agents = selected
            print(f"  {C.GREEN}✓ เลือก agents: {', '.join(selected)}{C.RESET}")
        self._show_active()

    def cmd_all(self):
        """/all - ใช้ทุก agent ที่ enabled"""
        if not self.enabled_ids:
            print(f"  {C.RED}ไม่มี agents ที่เปิดใช้งาน{C.RESET}")
            return
        self.active_agents = self.enabled_ids[:]
        names = ", ".join(self.enabled_ids)
        print(f"  {C.GREEN}✓ ใช้ทุก agents: {names}{C.RESET}")
        self._show_active()

    def cmd_none(self):
        """/none - ยกเลิกการเลือก"""
        self.active_agents = []
        print(f"  {C.YELLOW}ยกเลิกการเลือก agents{C.RESET}")
        self._show_active()

    def cmd_agents(self):
        """/agents - แสดง agents ทั้งหมด"""
        print(f"\n{C.BOLD}🤖 Agents ทั้งหมด:{C.RESET}")
        print(LINE)
        for aid, cfg in self.orch.agents_cfg.items():
            col = color_for(aid)
            enabled = f"{C.GREEN}✓ พร้อม{C.RESET}" if cfg.get("enabled") else f"{C.RED}✗ ปิด{C.RESET}"
            active = f" {C.CYAN}◄ active{C.RESET}" if aid in self.active_agents else ""
            to = cfg.get("timeout", "?")
            print(f"  {col}{aid.upper():<8}{C.RESET} | Timeout: {to}s | {enabled}{active}")
        print()

    def cmd_skills(self):
        """/skills - แสดง skills ทั้งหมด"""
        skills = self.skills.list_all()
        print(f"\n{C.BOLD}🎯 Skills ({len(skills)}):{C.RESET}")
        print(LINE)
        for s in skills:
            agents_str = ", ".join(s.agents)
            print(f"  {C.CYAN}{s.key:<20}{C.RESET} {s.description}")
            print(f"  {'':20} Agents: {agents_str} | Strategy: {s.strategy.value}")
            print()

    def cmd_run(self, args: str):
        """/run <skill_key> <prompt>"""
        parts = args.split(None, 1)
        if not parts:
            print(f"  {C.YELLOW}การใช้งาน: /run <skill> [prompt]{C.RESET}")
            self.cmd_skills()
            return

        skill_key = parts[0].lower()
        skill_prompt = parts[1] if len(parts) > 1 else ""

        skill = self.skills.get(skill_key)
        if not skill:
            print(f"  {C.RED}ไม่พบ skill '{skill_key}'{C.RESET}")
            self.cmd_skills()
            return

        # Security: Validate file path before reading
        if skill_prompt.startswith("@"):
            fpath = skill_prompt[1:].strip()
            if hasattr(self.orch, '_validate_file_read') and not self.orch._validate_file_read(fpath):
                print(f"  {C.RED}ไม่สามารถอ่านไฟล์: {fpath} (path ไม่ถูกต้อง){C.RESET}")
                return
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    file_content = f.read()
                skill_prompt = f"File: {fpath}\n\n{file_content}"
            except FileNotFoundError:
                print(f"  {C.RED}ไม่พบไฟล์: {fpath}{C.RESET}")
                return
            except Exception as e:
                print(f"  {C.RED}ข้อผิดพลาด: {e}{C.RESET}")
                return

        # เลือก agents
        agent_ids = self._resolve_skill_agents(skill)
        full_prompt = skill.get_full_prompt(skill_prompt)

        print(f"\n  {C.CYAN}🎯 Running skill: {skill.name}{C.RESET}")
        print(f"  Agents: {', '.join(agent_ids)} | Strategy: {skill.strategy.value}")
        print()

        # Execute by strategy
        if skill.strategy in (Strategy.SEQUENTIAL,):
            results = self.orch.sequential(agent_ids, full_prompt)
        else:
            results = self.orch.parallel(agent_ids, full_prompt)

        print_results(results)

        # Post-processing
        if skill.strategy == Strategy.PARALLEL_CONSENSUS:
            self._show_consensus_note(results)
        elif skill.strategy == Strategy.MAJORITY_VOTE:
            self._show_vote_note(results)
        elif skill.strategy == Strategy.PARALLEL_COMPARE:
            print_summary(results)

        self.orch.save_result(full_prompt, results, skill_key)

    def cmd_compare(self, prompt: str):
        """/compare - เปรียบเทียบผลทุก agent"""
        agents = self.active_agents or self.enabled_ids
        if not agents:
            print(f"  {C.RED}ไม่มี agents ที่เลือก{C.RESET}")
            return

        print(f"\n  {C.CYAN}📊 Comparing {len(agents)} agents...{C.RESET}\n")
        results = self.orch.parallel(agents, prompt)

        print(f"\n{C.BOLD}## ผลเปรียบเทียบ{C.RESET}\n")
        for r in results:
            col = color_for(r.agent_id)
            status = f"{C.GREEN}✓{C.RESET}" if r.success else f"{C.RED}✗{C.RESET}"
            print(f"### {status} {col}{r.agent_id.upper()}{C.RESET} ({r.elapsed:.1f}s)")
            print(LINE)
            if r.success:
                print(r.output)
            else:
                print(f"{C.RED}Error: {r.error}{C.RESET}")
            print()

        print_summary(results)
        self.orch.save_result(prompt, results, "compare")

    def cmd_consensus(self, prompt: str):
        """/consensus - หา consensus จากทุก agent"""
        agents = self.active_agents or self.enabled_ids
        if not agents:
            print(f"  {C.RED}ไม่มี agents ที่เลือก{C.RESET}")
            return

        print(f"\n  {C.CYAN}🤝 Generating consensus from {len(agents)} agents...{C.RESET}\n")
        results = self.orch.parallel(agents, prompt)

        print(f"\n{C.BOLD}📊 ผลลัพธ์:{C.RESET}")
        for r in results:
            col = color_for(r.agent_id)
            if r.success:
                print(f"  {C.GREEN}✓{C.RESET} {col}{r.agent_id.upper()}{C.RESET} ({r.elapsed:.1f}s) - {r.output[:120]}...")
            else:
                print(f"  {C.RED}✗{C.RESET} {r.agent_id.upper()} - Error: {r.error}")

        self._show_consensus_note(results)
        self.orch.save_result(prompt, results, "consensus")

    def cmd_help(self):
        print(f"""
{C.BOLD}📋 คำสั่งทั้งหมด:{C.RESET}
{LINE}
  {C.CYAN}/use <agent>{C.RESET}       เลือก agent เดียว เช่น /use qwen
  {C.CYAN}/use <a>,<b>{C.RESET}       เลือกหลาย agent เช่น /use codex,qwen
  {C.CYAN}/all{C.RESET}               ใช้ทุก agent พร้อมกัน
  {C.CYAN}/none{C.RESET}              ยกเลิกการเลือก
{LINE}
  {C.CYAN}/run <skill> [prompt]{C.RESET}  รัน skill เช่น /run code_review @file.py
  {C.CYAN}/compare <prompt>{C.RESET}      เปรียบเทียบผลทุก agent
  {C.CYAN}/consensus <prompt>{C.RESET}    หา consensus
{LINE}
  {C.CYAN}/agents{C.RESET}            แสดง agents ทั้งหมด
  {C.CYAN}/skills{C.RESET}            แสดง skills ทั้งหมด
  {C.CYAN}/clear{C.RESET}             ล้างหน้าจอ
  {C.CYAN}/help{C.RESET}              แสดงความช่วยเหลือ
  {C.CYAN}/exit{C.RESET}              ออก
{LINE}
  <prompt ปกติ>      ส่งไปยัง agents ที่เลือก
""")

    # ─── Helper ───────────────────────────────────────────────────────────────
    def _resolve_skill_agents(self, skill) -> list:
        """เลือก agents จาก skill (กรอง enabled)"""
        if self.active_agents:
            candidates = self.active_agents
        else:
            candidates = skill.agents

        result = [a for a in candidates if
                  a in self.orch.agents_cfg and
                  self.orch.agents_cfg[a].get("enabled", False)]

        if not result:
            # fallback: enabled agents
            result = self.enabled_ids[:2]
        return result

    def _show_consensus_note(self, results: list):
        ok = [r for r in results if r.success]
        if len(ok) >= 2:
            print(f"\n{C.BOLD}🤝 Consensus:{C.RESET}")
            print(LINE)
            print(f"  {len(ok)}/{len(results)} agents ตอบสำเร็จ")
            print(f"  รวมผลจาก: {', '.join(r.agent_id.upper() for r in ok)}")
            print()

    def _show_vote_note(self, results: list):
        ok = [r for r in results if r.success]
        print(f"\n{C.BOLD}🗳️  Majority Vote:{C.RESET}")
        print(LINE)
        print(f"  {len(ok)}/{len(results)} agents ตอบ — เปรียบเทียบด้วยตัวเองเพื่อหาคำตอบที่ดีที่สุด")
        print()

    # ─── Prompt dispatch ──────────────────────────────────────────────────────
    def _send(self, prompt: str):
        agents = self.active_agents
        if not agents:
            print(f"  {C.YELLOW}⚠️  ยังไม่ได้เลือก agent — พิมพ์ /all หรือ /use <agent>{C.RESET}\n")
            return

        if len(agents) == 1:
            col = color_for(agents[0])
            print(f"\n  {col}⏳ กำลังถาม {agents[0].upper()}...{C.RESET}\n")
            result = self.orch.single(agents[0], prompt)
            print_result(result)
            print()
            self.orch.save_result(prompt, [result], "single")
        else:
            print(f"\n  {C.CYAN}⚡ Running on {len(agents)} agents: {', '.join(agents)}{C.RESET}")
            print(LINE)
            results = self.orch.parallel(agents, prompt)
            print_results(results)
            self.orch.save_result(prompt, results, "parallel")

    # ─── Main loop ────────────────────────────────────────────────────────────
    def run(self):
        self._header()

        while True:
            try:
                prefix = self._prompt_prefix()
                user_input = input(f"{prefix} ➜  ").strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n  {C.DIM}Goodbye! 👋{C.RESET}\n")
                break

            if not user_input:
                continue

            lower = user_input.lower()

            # ─── Commands ─────────────────────────────────────────────────
            if lower in ("/exit", "/quit"):
                print(f"\n  {C.DIM}Goodbye! 👋{C.RESET}\n")
                break
            elif lower in ("/clear", "/cls"):
                os.system("cls" if os.name == "nt" else "clear")
                self._header()
            elif lower in ("/help", "/?"):
                self.cmd_help()
            elif lower == "/agents":
                self.cmd_agents()
            elif lower == "/skills":
                self.cmd_skills()
            elif lower in ("/all",):
                self.cmd_all()
            elif lower in ("/none",):
                self.cmd_none()
            elif lower.startswith("/use "):
                self.cmd_use(user_input[5:].strip())
            elif lower == "/use":
                self.cmd_use("")
            elif lower.startswith("/run "):
                self.cmd_run(user_input[5:].strip())
            elif lower.startswith("/compare "):
                self.cmd_compare(user_input[9:].strip())
            elif lower.startswith("/consensus "):
                self.cmd_consensus(user_input[11:].strip())
            elif lower.startswith("/"):
                # ลอง parse เป็น /agent_name (ทางลัด)
                cmd = lower[1:].split()[0]
                if cmd in self.orch.agents_cfg:
                    self.cmd_use(cmd)
                else:
                    print(f"  {C.RED}ไม่รู้จักคำสั่ง '{user_input}' — พิมพ์ /help{C.RESET}")
            else:
                # Plain prompt → send to active agents
                self._send(user_input)


def main():
    import ctypes
    if os.name == "nt":
        try:
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7
            )
        except Exception:
            pass
    cli = InteractiveCLI()
    cli.run()


if __name__ == "__main__":
    main()
