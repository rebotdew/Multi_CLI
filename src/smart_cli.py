"""
smart_cli.py - Modern & Friendly Interactive CLI
ออกแบบมาให้ใช้งานง่ายสำหรับทุกคน (Style 3)
"""
import sys
import os
import time
import threading
import itertools
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import Orchestrator, C, color_for, print_result, print_results, print_summary, LINE
from controller import auto_route, Controller
from skills_registry import SkillsRegistry
from utils import get_visual_width, print_header

class SmartCLI(Controller):
    def __init__(self):
        super().__init__()
        self.stop_spinner = False

    def _header(self):
        print_header()
        
        # แสดงสถานะ Agents แบบกะทัดรัด
        enabled = [a.upper() for a in self.enabled_ids]
        print(f" {C.DIM}● Ready Agents: {', '.join(enabled)}{C.RESET}\n")
        self._show_active_status()

    def _show_active_status(self):
        if not self.selected:
            print(f"  {C.YELLOW}📌 Active: [Auto Mode] — ระบบจะเลือก AI ให้เอง{C.RESET}\n")
        else:
            names = ", ".join(a.upper() for a in self.selected)
            print(f"  {C.GREEN}📌 Active: {names}{C.RESET}\n")

    def _spinner(self, message="กำลังคิด..."):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while not self.stop_spinner:
            sys.stdout.write(f'\r {C.YELLOW}{next(spinner)}{C.RESET} {message} ')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')

    def _show_progress_bar(self):
        """แสดงแถบโหลดแบบสวยๆ หลังเสร็จงาน"""
        print(f" {C.GREEN}[{'█'*20}]{C.RESET} 100% (เสร็จสิ้น!)")

    def _send(self, prompt: str):
        # ตรวจสอบว่ามีชื่อไฟล์ใน prompt ไหม (Auto-file detection)
        words = prompt.split()
        potential_file = ""
        for w in words:
            if "." in w and os.path.isfile(w):
                potential_file = w
                break
        
        if potential_file and "@" not in prompt:
            print(f" {C.YELLOW}📂 ตรวจพบไฟล์: {potential_file}{C.RESET}")
            confirm = input(f" {C.DIM}➜ ต้องการให้ AI อ่านไฟล์นี้ด้วยไหม? (y/n): {C.RESET}").lower()
            if confirm == 'y':
                try:
                    with open(potential_file, "r", encoding="utf-8") as f:
                        prompt = f"File: {potential_file}\n\nContent:\n{f.read()}\n\nQuestion: {prompt}"
                except:
                    print(f" {C.RED}✗ อ่านไฟล์ไม่ได้{C.RESET}")

        self.stop_spinner = False
        spinner_thread = threading.Thread(target=self._spinner)
        spinner_thread.start()

        try:
            if self.selected:
                agents = [a for a in self.selected if self.orch.agents_cfg[a].get("enabled", False)]
                if len(agents) == 1:
                    result = self.orch.single(agents[0], prompt)
                    self.stop_spinner = True
                    spinner_thread.join()
                    self._show_progress_bar()
                    print_result(result)
                    self.orch.save_result(prompt, [result], "single")
                else:
                    results = self.orch.parallel(agents, prompt)
                    self.stop_spinner = True
                    spinner_thread.join()
                    self._show_progress_bar()
                    print_results(results)
                    self.orch.save_result(prompt, results, "parallel")
            else:
                chosen = auto_route(prompt, self.orch.agents_cfg)
                result = self.orch.single(chosen, prompt)
                self.stop_spinner = True
                spinner_thread.join()
                
                col = color_for(chosen)
                print(f" {C.DIM}📝 Auto-route → {col}{chosen.upper()}{C.RESET}")
                self._show_progress_bar()
                print_result(result)
                self.orch.save_result(prompt, [result], f"auto:{chosen}")
        except Exception as e:
            self.stop_spinner = True
            print(f"\n {C.RED}✗ เกิดข้อผิดพลาด: {e}{C.RESET}")

    def run(self):
        self._header()
        while True:
            try:
                mode = f"[{','.join(self.selected)}]" if self.selected else "[Auto]"
                user_input = input(f"{C.CYAN}{mode}{C.RESET} {C.BOLD}➜{C.RESET}  ").strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n {C.DIM}บ๊ายบาย! 👋{C.RESET}\n")
                break

            if not user_input: continue
            lower = user_input.lower()

            if lower in ("/exit", "/quit"): break
            elif lower in ("/clear", "/cls"): self._header()
            elif lower.startswith("/"):
                # จัดการคำสั่งแบบ Shorthand
                if lower == "/help": self.cmd_help()
                elif lower.startswith("/use "): self.cmd_use(user_input[5:])
                elif lower.startswith("/run "): self.cmd_run(user_input[5:])
                elif lower == "/status": self.cmd_status()
                else:
                    # ถ้าใส่ /name ให้ถือว่าเป็น /use name
                    agent_cmd = lower[1:].split()[0]
                    if agent_cmd in self.orch.agents_cfg:
                        self.cmd_use(agent_cmd)
                    else:
                        print(f" {C.RED}✗ ไม่รู้จักคำสั่ง '{user_input}'{C.RESET}")
            else:
                self._send(user_input)

if __name__ == "__main__":
    cli = SmartCLI()
    cli.run()
