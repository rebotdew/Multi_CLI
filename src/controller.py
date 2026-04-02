"""
controller.py (= run_controller.py) - Central Control Agent
Auto-routing + /to + /broadcast + /run skill + /use
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import Orchestrator, C, color_for, print_result, print_results, print_summary, LINE
from skills_registry import SkillsRegistry, Strategy
from utils import print_header


# ─── Auto-routing rules (keyword → agent_id) ──────────────────────────────────
ROUTING_RULES = [
    # Code
    (["code", "โค้ด", "function", "bug", "debug", "fix", "error", "refactor",
      "review", "python", "javascript", "typescript", "class", "def ", "เขียน code",
      "เขียนโค้ด", "แก้", "test", "security"], "codex"),

    # Math / Analysis / Thai
    (["math", "คณิต", "สมการ", "วิเคราะห์", "analysis", "เปรียบเทียบ", "อธิบาย",
      "explain", "reasoning", "ทำไม", "เพราะ", "สรุป document", "เอกสาร"], "kimi"),

    # Thai / Translate
    (["แปล", "translate", "ภาษาไทย", "ภาษา", "thai", "ความหมาย",
      "summarize", "สรุป", "สั้น", "ย่อ"], "qwen"),
]

DEFAULT_AGENT = "qwen"


def auto_route(prompt: str, agents_cfg: dict) -> str:
    """เลือก agent ที่เหมาะสมจาก keyword"""
    p = prompt.lower()
    for keywords, agent_id in ROUTING_RULES:
        if any(kw in p for kw in keywords):
            if agent_id in agents_cfg and agents_cfg[agent_id].get("enabled", False):
                return agent_id
    # fallback: default หรือ agent enabled แรก
    if DEFAULT_AGENT in agents_cfg and agents_cfg[DEFAULT_AGENT].get("enabled", False):
        return DEFAULT_AGENT
    for aid, cfg in agents_cfg.items():
        if cfg.get("enabled", False):
            return aid
    return list(agents_cfg.keys())[0]


class Controller:
    def __init__(self):
        self.orch = Orchestrator()
        self.skills = SkillsRegistry()
        self.selected: list = []        # ว่าง = auto mode
        self.enabled_ids = list(self.orch.get_enabled_agents().keys())
        self.all_ids = list(self.orch.agents_cfg.keys())

    # ─── Header ───────────────────────────────────────────────────────────────
    def _header(self):
        print_header()
        
        enabled = [a.upper() for a in self.enabled_ids]
        print(f" {C.DIM}● Ready Agents: {', '.join(enabled)}{C.RESET}\n")
        self._show_active()

    def _show_active(self):
        if not self.selected:
            print(f"  {C.YELLOW}📌 Active: [Auto Mode] — ระบบจะเลือก AI ให้เอง{C.RESET}\n")
        else:
            names = ", ".join(a.upper() for a in self.selected)
            print(f"  {C.GREEN}📌 Active: {names}{C.RESET}\n")


    def _prompt_prefix(self) -> str:
        if not self.selected:
            return f"{C.DIM}[auto]{C.RESET}"
        if len(self.selected) == len(self.all_ids):
            return f"{C.CYAN}[all]{C.RESET}"
        names = ",".join(self.selected)
        return f"{C.GREEN}[{names}]{C.RESET}"

    # ─── Commands ─────────────────────────────────────────────────────────────
    def cmd_use(self, args: str):
        """/use none|all|<agent>|<a>,<b>"""
        if not args:
            print(f"  {C.YELLOW}การใช้งาน: /use <agent> | /use all | /use none{C.RESET}\n")
            return

        arg = args.strip().lower()
        if arg == "none":
            self.selected = []
            print(f"  {C.YELLOW}✓ Auto mode (router จะเลือกเอง){C.RESET}")
        elif arg == "all":
            self.selected = self.enabled_ids[:]
            print(f"  {C.GREEN}✓ เลือกทุก agent: {', '.join(self.selected)}{C.RESET}")
        else:
            chosen = [a.strip() for a in arg.split(",")]
            valid = []
            for aid in chosen:
                if aid not in self.orch.agents_cfg:
                    print(f"  {C.RED}ไม่รู้จัก '{aid}'{C.RESET}")
                elif not self.orch.agents_cfg[aid].get("enabled", False):
                    print(f"  {C.YELLOW}⚠️  {aid} ปิดอยู่{C.RESET}")
                else:
                    valid.append(aid)
            if valid:
                self.selected = valid
                print(f"  {C.GREEN}✓ เลือก: {', '.join(valid)}{C.RESET}")

        self._show_active()

    def cmd_to(self, args: str):
        """/to <agent> <prompt>"""
        parts = args.split(None, 1)
        if len(parts) < 2:
            print(f"  {C.YELLOW}การใช้งาน: /to <agent> <prompt>{C.RESET}\n")
            return

        agent_id, prompt = parts[0].lower(), parts[1]

        if agent_id not in self.orch.agents_cfg:
            print(f"  {C.RED}ไม่รู้จัก '{agent_id}'{C.RESET}\n")
            return
        if not self.orch.agents_cfg[agent_id].get("enabled", False):
            print(f"  {C.YELLOW}⚠️  {agent_id} ปิดอยู่{C.RESET}\n")
            return

        col = color_for(agent_id)
        print(f"\n  {C.CYAN}➤ Sending to {col}{agent_id.upper()}{C.RESET}...\n")
        result = self.orch.single(agent_id, prompt)
        print_result(result)
        print()
        self.orch.save_result(prompt, [result], f"to:{agent_id}")

    def cmd_broadcast(self, prompt: str):
        """/broadcast <prompt>"""
        agents = self.selected or self.enabled_ids
        if not agents:
            print(f"  {C.RED}ไม่มี agents ที่เปิดใช้งาน{C.RESET}\n")
            return

        print(f"\n  {C.CYAN}📢 Broadcasting to {len(agents)} agents: {', '.join(a.upper() for a in agents)}{C.RESET}\n")
        results = self.orch.parallel(agents, prompt)
        print_results(results)
        print_summary(results)
        self.orch.save_result(prompt, results, "broadcast")

    def cmd_run(self, args: str):
        """/run <skill> [prompt | @file]"""
        parts = args.split(None, 1)
        if not parts:
            self._show_skills()
            return

        skill_key = parts[0].lower()
        skill_prompt = parts[1] if len(parts) > 1 else ""

        skill = self.skills.get(skill_key)
        if not skill:
            print(f"  {C.RED}ไม่พบ skill '{skill_key}'{C.RESET}")
            self._show_skills()
            return

        # Security: Validate file path before reading
        if skill_prompt.startswith("@"):
            fpath = skill_prompt[1:].strip()
            if hasattr(self.orch, '_validate_file_read') and not self.orch._validate_file_read(fpath):
                print(f"  {C.RED}ไม่สามารถอ่านไฟล์: {fpath} (path ไม่ถูกต้อง){C.RESET}\n")
                return
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    skill_prompt = f"File: {fpath}\n\n{f.read()}"
            except FileNotFoundError:
                print(f"  {C.RED}ไม่พบไฟล์: {fpath}{C.RESET}\n")
                return
            except Exception as e:
                print(f"  {C.RED}ข้อผิดพลาด: {e}{C.RESET}\n")
                return

        # เลือก agents
        if self.selected:
            agents = [a for a in self.selected
                      if self.orch.agents_cfg[a].get("enabled", False)]
        else:
            agents = [a for a in skill.agents
                      if a in self.orch.agents_cfg and
                      self.orch.agents_cfg[a].get("enabled", False)]
        if not agents:
            agents = self.enabled_ids[:2]

        full_prompt = skill.get_full_prompt(skill_prompt)

        print(f"\n  {C.CYAN}🎯 Running skill: {skill.name}{C.RESET}")
        print(f"  Strategy: {skill.strategy.value} | Agents: {', '.join(agents)}\n")

        if skill.strategy.value == "sequential":
            results = self.orch.sequential(agents, full_prompt)
        else:
            results = self.orch.parallel(agents, full_prompt)

        print_results(results)
        print_summary(results)
        self.orch.save_result(full_prompt, results, skill_key)

    def cmd_status(self):
        print(f"\n{C.BOLD}📊 Agent Status:{C.RESET}")
        print(LINE)
        for aid, cfg in self.orch.agents_cfg.items():
            col = color_for(aid)
            status = f"{C.GREEN}✓ พร้อม{C.RESET}" if cfg.get("enabled") else f"{C.RED}✗ ปิด{C.RESET}"
            active = f" {C.CYAN}◄{C.RESET}" if aid in self.selected else ""
            print(f"  {col}{aid.upper():<8}{C.RESET} | {status} | Timeout: {cfg.get('timeout','?')}s{active}")
        mode = f"[{', '.join(self.selected)}]" if self.selected else "[auto]"
        print(f"\n  Mode: {C.BOLD}{mode}{C.RESET}\n")

    def _show_skills(self):
        print(f"\n{C.BOLD}🎯 Skills ที่มี:{C.RESET}")
        for s in self.skills.list_all():
            print(f"  {C.CYAN}{s.key:<20}{C.RESET} {s.description}")
        print()

    def cmd_help(self):
        print(f"""
{C.BOLD}📋 คำสั่ง AIC:{C.RESET}
{LINE}
  {C.CYAN}/use <agent>{C.RESET}            เลือก agent (/use qwen)
  {C.CYAN}/use <a>,<b>{C.RESET}            เลือกหลาย agent
  {C.CYAN}/use all{C.RESET}                เลือกทุก agent
  {C.CYAN}/use none{C.RESET}               Auto mode (router เลือกให้)
{LINE}
  {C.CYAN}/to <agent> <prompt>{C.RESET}    ส่งตรงไป agent นั้น
  {C.CYAN}/broadcast <prompt>{C.RESET}     ส่งทุก agent
  {C.CYAN}/run <skill> [prompt]{C.RESET}   รัน skill
  {C.CYAN}/skills{C.RESET}                 ดู skills ทั้งหมด
{LINE}
  {C.CYAN}/status{C.RESET}                 สถานะ agents
  {C.CYAN}/clear{C.RESET}                  ล้างหน้าจอ
  {C.CYAN}/help{C.RESET}                   ความช่วยเหลือ
  {C.CYAN}/exit{C.RESET}                   ออก
{LINE}
  <prompt ปกติ>           ส่งผ่าน auto-router หรือ agents ที่เลือก
""")

    # ─── Auto-routing + send ──────────────────────────────────────────────────
    def _send(self, prompt: str):
        if self.selected:
            agents = [a for a in self.selected
                      if self.orch.agents_cfg[a].get("enabled", False)]
            if not agents:
                print(f"  {C.RED}agents ที่เลือกปิดอยู่{C.RESET}\n")
                return

            if len(agents) == 1:
                col = color_for(agents[0])
                print(f"\n  {col}⏳ {agents[0].upper()}...{C.RESET}\n")
                result = self.orch.single(agents[0], prompt)
                print_result(result)
                print()
                self.orch.save_result(prompt, [result], "single")
            else:
                print(f"\n  {C.CYAN}⚡ Running {len(agents)} agents: {', '.join(a.upper() for a in agents)}{C.RESET}\n")
                results = self.orch.parallel(agents, prompt)
                print_results(results)
                self.orch.save_result(prompt, results, "parallel")
        else:
            # Auto route
            chosen = auto_route(prompt, self.orch.agents_cfg)
            col = color_for(chosen)
            print(f"\n  {C.DIM}📝 Auto-routing → {col}{chosen.upper()}{C.RESET}\n")
            result = self.orch.single(chosen, prompt)
            print_result(result)
            print()
            self.orch.save_result(prompt, [result], f"auto:{chosen}")

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

            if lower in ("/exit", "/quit"):
                print(f"\n  {C.DIM}Goodbye! 👋{C.RESET}\n")
                break
            elif lower in ("/clear", "/cls"):
                os.system("cls" if os.name == "nt" else "clear")
                self._header()
            elif lower in ("/help", "/?"):
                self.cmd_help()
            elif lower in ("/status", "/agents"):
                self.cmd_status()
            elif lower == "/skills":
                self._show_skills()
            elif lower.startswith("/use "):
                self.cmd_use(user_input[5:].strip())
            elif lower == "/use":
                self.cmd_use("")
            elif lower.startswith("/to "):
                self.cmd_to(user_input[4:].strip())
            elif lower.startswith("/broadcast "):
                self.cmd_broadcast(user_input[11:].strip())
            elif lower.startswith("/bc "):
                self.cmd_broadcast(user_input[4:].strip())
            elif lower.startswith("/run "):
                self.cmd_run(user_input[5:].strip())
            elif lower.startswith("/"):
                # ลอง /agent_name เป็น /use shortcut
                cmd = lower[1:].split()[0]
                if cmd in self.orch.agents_cfg:
                    self.cmd_use(cmd)
                else:
                    print(f"  {C.RED}ไม่รู้จักคำสั่ง — พิมพ์ /help{C.RESET}")
            else:
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
    ctl = Controller()
    ctl.run()


if __name__ == "__main__":
    main()
