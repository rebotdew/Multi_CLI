"""
aiswitch.py - AI Switch
วิธีง่ายที่สุด: เลือก AI ด้วย /qwen /kimi /codex /gemini แล้วพิมพ์ข้อความ
"""
import sys
import os
import asyncio
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import Orchestrator, C, color_for, print_result, print_results, LINE
from utils import print_header

# Speed labels
SPEED_LABELS = {
    "qwen":   ("10-40s",  "⭐⭐⭐⭐⭐"),
    "kimi":   ("45-80s",  "⭐⭐⭐"),
    "codex":  ("15-25s",  "⭐⭐⭐⭐"),
    "gemini": ("120s+",   "⭐"),
}

AGENT_DESC = {
    "qwen":   "เร็วสุด  ใช้งานทั่วไป",
    "kimi":   "ภาษาไทย เก่งอธิบาย",
    "codex":  "เก่งโค้ด debug",
    "gemini": "ฉลาด   งานซับซ้อน",
}


class AISwitch:
    def __init__(self):
        self.orch = Orchestrator()
        self.current = self.orch.settings.get("default_agent", "qwen")
        self.all_agents = list(self.orch.agents_cfg.keys())
        self.enabled = list(self.orch.get_enabled_agents().keys())

    def _header(self):
        print_header("🤖 AI Switch - เลือก AI ง่ายๆ", 
                     "เลือก AI ด้วยคำสั่ง /<name> เช่น /qwen /kimi")
        
        agents_cfg = self.orch.agents_cfg
        for aid in self.all_agents:
            cfg = agents_cfg[aid]
            enabled = cfg.get("enabled", False)
            col = color_for(aid)
            speed, stars = SPEED_LABELS.get(aid, ("?", "?"))
            desc = AGENT_DESC.get(aid, "")

            if aid == self.current and self.current != "all":
                marker = f"{C.GREEN}✅{C.RESET}"
                active = f" {C.GREEN}◄ ACTIVE{C.RESET}"
            elif not enabled:
                marker = f"{C.DIM}❌{C.RESET}"
                active = f" {C.DIM}(disabled){C.RESET}"
            else:
                marker = "  "
                active = ""

            print(f"  {marker} {col}/{aid:<8}{C.RESET} - {desc:<20} ({speed}) {stars}{active}")

        if self.current == "all":
            print(f"  {C.GREEN}✅ /all{C.RESET}   - ใช้ทุก AI พร้อมกัน            {C.GREEN}◄ ACTIVE{C.RESET}")
        else:
            print(f"     /all    - ใช้ทุก AI พร้อมกัน")

        print(f"\n  {C.DIM}/exit - ออก  |  /status - สถานะ  |  /clear - ล้างจอ{C.RESET}\n")

    def _prompt_prefix(self) -> str:
        col = color_for(self.current) if self.current != "all" else C.CYAN
        return f"{col}[{self.current}]{C.RESET}"

    def _switch(self, target: str) -> bool:
        if target == "all":
            self.current = "all"
            print(f"\n  {C.GREEN}✓ ใช้ทุก AI: {', '.join(self.enabled)}{C.RESET}\n")
            return True

        if target not in self.orch.agents_cfg:
            print(f"\n  {C.RED}ไม่รู้จัก AI '{target}' — รองรับ: {', '.join(self.all_agents)}{C.RESET}\n")
            return False

        if not self.orch.agents_cfg[target].get("enabled", False):
            print(f"\n  {C.YELLOW}⚠️  {target.upper()} ปิดอยู่ — แก้ config.json ให้ enabled: true{C.RESET}\n")
            return False

        self.current = target
        col = color_for(target)
        print(f"\n  {C.GREEN}✓ เปลี่ยนเป็น {col}{target.upper()}{C.RESET}\n")
        return True

    def _send(self, prompt: str):
        if self.current == "all":
            if not self.enabled:
                print(f"{C.RED}ไม่มี AI ที่เปิดใช้งาน{C.RESET}")
                return
            print(f"\n  {C.CYAN}⚡ Running ALL {len(self.enabled)} agents...{C.RESET}\n")
            results = self.orch.parallel(self.enabled, prompt)
            print_results(results)
            self.orch.save_result(prompt, results, "broadcast")
        else:
            if self.current not in self.orch.agents_cfg:
                print(f"{C.RED}ไม่พบ '{self.current}'{C.RESET}")
                return
            col = color_for(self.current)
            print(f"\n  {col}⏳ กำลังถาม {self.current.upper()}...{C.RESET}\n")
            result = self.orch.single(self.current, prompt)
            print_result(result)
            print()
            self.orch.save_result(prompt, [result], "single")

    def _status(self):
        agents_cfg = self.orch.agents_cfg
        print(f"\n{C.BOLD}🤖 สถานะ Agents:{C.RESET}")
        print(LINE)
        for aid, cfg in agents_cfg.items():
            col = color_for(aid)
            enabled = "✅ พร้อม" if cfg.get("enabled") else "❌ ปิด"
            to = cfg.get("timeout", "?")
            print(f"  {col}{aid.upper():<8}{C.RESET} | Timeout: {to}s | {enabled}")
        print(f"\n  📌 ใช้อยู่: {C.BOLD}{self.current.upper()}{C.RESET}\n")

    def run(self):
        self._header()
        print(f"  📌 Using: {C.BOLD}{self.current.upper()}{C.RESET}\n")

        while True:
            try:
                prefix = self._prompt_prefix()
                user_input = input(f"\n{prefix} ▶ ").strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n  {C.DIM}Goodbye! 👋{C.RESET}\n")
                break

            if not user_input:
                continue

            lower = user_input.lower()

            # Commands
            if lower in ("/exit", "/quit", "q", "quit", "exit"):
                print(f"\n  {C.DIM}Goodbye! 👋{C.RESET}\n")
                break
            elif lower in ("/clear", "/cls"):
                self._header()
            elif lower in ("/status", "/agents"):
                self._status()
            elif lower in ("/help", "/?"):
                self._header()
            elif lower.startswith("/"):
                cmd = lower[1:].strip()
                self._switch(cmd)
            else:
                self._send(user_input)


def main():
    import ctypes
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )
    sw = AISwitch()
    sw.run()


if __name__ == "__main__":
    main()
