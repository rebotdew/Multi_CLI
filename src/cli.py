"""
cli.py - Command Mode
multi-ai run code_review "@file.py"
multi-ai exec "prompt" --agents codex,qwen
multi-ai list skills
multi-ai consensus "question"
multi-ai compare "prompt"
multi-ai config --show
"""
import sys
import os
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import Orchestrator, C, color_for, print_result, print_results, print_summary, LINE
from skills_registry import SkillsRegistry, Strategy


orch = Orchestrator()
skills_reg = SkillsRegistry()


# ─── List ─────────────────────────────────────────────────────────────────────
def cmd_list(args):
    target = args.target if hasattr(args, "target") else "skills"

    if target == "skills":
        skills = skills_reg.list_all()
        print(f"\n{C.BOLD}🎯 Skills ({len(skills)}):{C.RESET}")
        print(LINE)
        for s in skills:
            print(f"  {C.CYAN}{s.key:<22}{C.RESET} {s.description}")
            print(f"  {'':22} Agents: {', '.join(s.agents)} | {s.strategy.value}")
            print()

    elif target == "agents":
        print(f"\n{C.BOLD}🤖 Agents:{C.RESET}")
        print(LINE)
        for aid, cfg in orch.agents_cfg.items():
            col = color_for(aid)
            status = f"{C.GREEN}✓ enabled{C.RESET}" if cfg.get("enabled") else f"{C.RED}✗ disabled{C.RESET}"
            print(f"  {col}{aid.upper():<10}{C.RESET} | {status} | timeout: {cfg.get('timeout','?')}s")
        print()


# ─── Run skill ────────────────────────────────────────────────────────────────
def cmd_run(args):
    skill_key = args.skill
    prompt_raw = " ".join(args.prompt) if args.prompt else ""
    agent_filter = [a.strip() for a in args.agents.split(",")] if args.agents else None

    skill = skills_reg.get(skill_key)
    if not skill:
        print(f"{C.RED}ไม่พบ skill '{skill_key}'{C.RESET}")
        cmd_list(type("A", (), {"target": "skills"})())
        sys.exit(1)

    # Read file if @file (with security validation)
    if prompt_raw.startswith("@"):
        fpath = prompt_raw[1:].strip()
        orch_instance = orch  # Reference to orchestrator
        if hasattr(orch_instance, '_validate_file_read') and not orch_instance._validate_file_read(fpath):
            print(f"{C.RED}ไม่สามารถอ่านไฟล์: {fpath} (path ไม่ถูกต้อง หรือ extension ไม่อนุญาต){C.RESET}")
            sys.exit(1)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                prompt_raw = f"File: {fpath}\n\n{f.read()}"
        except FileNotFoundError:
            print(f"{C.RED}ไม่พบไฟล์: {fpath}{C.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{C.RED}ข้อผิดพลาดในการอ่านไฟล์: {e}{C.RESET}")
            sys.exit(1)

    # Resolve agents
    if agent_filter:
        agent_ids = [a for a in agent_filter
                     if a in orch.agents_cfg and orch.agents_cfg[a].get("enabled", False)]
    else:
        agent_ids = [a for a in skill.agents
                     if a in orch.agents_cfg and orch.agents_cfg[a].get("enabled", False)]

    if not agent_ids:
        print(f"{C.YELLOW}ไม่มี agents ที่พร้อมใช้งาน — เช็ค config.json{C.RESET}")
        sys.exit(1)

    full_prompt = skill.get_full_prompt(prompt_raw)

    print(f"\n{C.BOLD}🎯 Skill: {skill.name}{C.RESET}")
    print(f"   Strategy: {skill.strategy.value} | Agents: {', '.join(agent_ids)}\n")

    if skill.strategy.value == "sequential":
        results = orch.sequential(agent_ids, full_prompt)
    else:
        results = orch.parallel(agent_ids, full_prompt)

    print_results(results, show_cmd=getattr(args, "verbose", False))
    print_summary(results)
    orch.save_result(full_prompt, results, skill_key)


# ─── Exec ─────────────────────────────────────────────────────────────────────
def cmd_exec(args):
    prompt = " ".join(args.prompt)
    agent_filter = [a.strip() for a in args.agents.split(",")] if args.agents else None
    sequential = getattr(args, "sequential", False)

    enabled = orch.get_enabled_agents()
    if agent_filter:
        agent_ids = [a for a in agent_filter if a in enabled]
    else:
        agent_ids = list(enabled.keys())

    if not agent_ids:
        print(f"{C.RED}ไม่มี agents พร้อมใช้{C.RESET}")
        sys.exit(1)

    print(f"\n{C.CYAN}{'Sequential' if sequential else 'Parallel'}: {', '.join(a.upper() for a in agent_ids)}{C.RESET}\n")

    if sequential:
        results = orch.sequential(agent_ids, prompt)
    else:
        results = orch.parallel(agent_ids, prompt)

    print_results(results, show_cmd=getattr(args, "verbose", False))
    print_summary(results)
    orch.save_result(prompt, results, "exec")


# ─── Consensus ────────────────────────────────────────────────────────────────
def cmd_consensus(args):
    prompt = " ".join(args.prompt)
    enabled = orch.get_enabled_agents()
    agent_ids = list(enabled.keys())

    if not agent_ids:
        print(f"{C.RED}ไม่มี agents พร้อมใช้{C.RESET}")
        sys.exit(1)

    print(f"\n{C.CYAN}🤝 Consensus จาก {len(agent_ids)} agents...{C.RESET}\n")
    results = orch.parallel(agent_ids, prompt)

    print(f"{C.BOLD}📊 ผลลัพธ์:{C.RESET}")
    for r in results:
        col = color_for(r.agent_id)
        if r.success:
            preview = r.output[:150].replace("\n", " ")
            print(f"  {C.GREEN}✓{C.RESET} {col}{r.agent_id.upper()}{C.RESET} ({r.elapsed:.1f}s) — {preview}...")
        else:
            print(f"  {C.RED}✗{C.RESET} {r.agent_id.upper()} — {r.error}")

    print(f"\n{C.BOLD}🤝 Consensus:{C.RESET}")
    print(LINE)
    ok = [r for r in results if r.success]
    print(f"  {len(ok)}/{len(results)} agents ตอบสำเร็จ — เปรียบเทียบคำตอบด้านบนเพื่อสรุป")
    print()
    orch.save_result(prompt, results, "consensus")


# ─── Compare ──────────────────────────────────────────────────────────────────
def cmd_compare(args):
    prompt = " ".join(args.prompt)
    agent_filter = [a.strip() for a in args.agents.split(",")] if args.agents else None
    enabled = orch.get_enabled_agents()

    if agent_filter:
        agent_ids = [a for a in agent_filter if a in enabled]
    else:
        agent_ids = list(enabled.keys())

    if not agent_ids:
        print(f"{C.RED}ไม่มี agents พร้อมใช้{C.RESET}")
        sys.exit(1)

    print(f"\n{C.CYAN}📊 เปรียบเทียบ {len(agent_ids)} agents:{C.RESET}\n")
    results = orch.parallel(agent_ids, prompt)

    print(f"\n{C.BOLD}## ผลเปรียบเทียบ{C.RESET}\n")
    for r in results:
        col = color_for(r.agent_id)
        print(f"### {col}{r.agent_id.upper()}{C.RESET} ({r.elapsed:.1f}s)")
        print(LINE)
        if r.success:
            print(r.output)
        else:
            print(f"{C.RED}Error: {r.error}{C.RESET}")
        print()

    print_summary(results)
    orch.save_result(prompt, results, "compare")


# ─── Config ───────────────────────────────────────────────────────────────────
def cmd_config(args):
    if getattr(args, "show", False) or True:
        cfg_path = Path(__file__).parent / "config.json"
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"\n{C.BOLD}⚙️  Config: {cfg_path}{C.RESET}\n")
        for aid, cfg in data["agents"].items():
            col = color_for(aid)
            status = f"{C.GREEN}enabled{C.RESET}" if cfg.get("enabled") else f"{C.RED}disabled{C.RESET}"
            print(f"  {col}{aid:<8}{C.RESET} {status} | cmd: {cfg['cmd']} | timeout: {cfg.get('timeout','?')}s")

        print(f"\n{C.DIM}{json.dumps(data['settings'], ensure_ascii=False, indent=2)}{C.RESET}\n")


# ─── Parser ───────────────────────────────────────────────────────────────────
def build_parser():
    parser = argparse.ArgumentParser(
        prog="multi-ai",
        description="Multi-Agent AI CLI Controller",
    )
    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="แสดง skills หรือ agents")
    p_list.add_argument("target", choices=["skills", "agents"], default="skills", nargs="?")

    # run
    p_run = sub.add_parser("run", help="รัน skill")
    p_run.add_argument("skill", help="ชื่อ skill เช่น code_review")
    p_run.add_argument("prompt", nargs="*", help="prompt หรือ @file")
    p_run.add_argument("--agents", help="เลือก agents เช่น codex,qwen")
    p_run.add_argument("--verbose", "-v", action="store_true")

    # exec
    p_exec = sub.add_parser("exec", help="รัน prompt โดยตรง")
    p_exec.add_argument("prompt", nargs="+", help="prompt ที่จะส่ง")
    p_exec.add_argument("--agents", help="เลือก agents")
    p_exec.add_argument("--parallel", action="store_true", default=True)
    p_exec.add_argument("--sequential", action="store_true")
    p_exec.add_argument("--verbose", "-v", action="store_true")

    # consensus
    p_con = sub.add_parser("consensus", help="หา consensus")
    p_con.add_argument("prompt", nargs="+")

    # compare
    p_cmp = sub.add_parser("compare", help="เปรียบเทียบผลลัพธ์")
    p_cmp.add_argument("prompt", nargs="+")
    p_cmp.add_argument("--agents", help="เลือก agents")

    # config
    p_cfg = sub.add_parser("config", help="จัดการ config")
    p_cfg.add_argument("--show", action="store_true")

    return parser


def main():
    import ctypes
    if os.name == "nt":
        try:
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7
            )
        except Exception:
            pass

    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    dispatch = {
        "list":      cmd_list,
        "run":       cmd_run,
        "exec":      cmd_exec,
        "consensus": cmd_consensus,
        "compare":   cmd_compare,
        "config":    cmd_config,
    }
    fn = dispatch.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
