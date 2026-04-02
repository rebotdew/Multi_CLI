"""
wizard.py - Interactive Configuration Wizard
Uses prompt-toolkit for a rich setup experience.
"""
import json
import os
import shutil
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm, radiolist_dialog, input_dialog, message_dialog
from prompt_toolkit.styles import Style

from orchestrator import C
from utils import print_header

CONFIG_PATH = Path(__file__).parent / "config.json"

style = Style.from_dict({
    'dialog': 'bg:#0000aa',
    'dialog frame.label': 'bg:#ffffff #000000',
    'dialog.body': 'bg:#000000 #ffffff',
    'dialog shadow': 'bg:#000000',
})

def run_wizard():
    print_header("🪄 MULTI-AI CONFIG WIZARD", "ยินดีต้อนรับสู่ระบบตั้งค่า Multi_CLI")
    
    if not CONFIG_PATH.exists():
        data = {
            "agents": {},
            "settings": {
                "default_timeout": 180,
                "max_retries": 1,
                "save_outputs": True,
                "max_output_chars": 10000,
                "output_dir": "output",
                "log_dir": "logs",
                "default_agent": ""
            }
        }
    else:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

    while True:
        choice = radiolist_dialog(
            title="Main Menu",
            text="เลือกหัวข้อที่ต้องการจัดการ:",
            values=[
                ("agents", "🤖 จัดการ AI Agents (เพิ่ม/ลบ/แก้ไข)"),
                ("settings", "⚙️  ตั้งค่าระบบ (Timeout, Output, etc.)"),
                ("save", "💾 บันทึกและออก"),
                ("exit", "❌ ออกโดยไม่บันทึก")
            ],
            style=style
        ).run()

        if choice == "agents":
            data = manage_agents(data)
        elif choice == "settings":
            data = manage_settings(data)
        elif choice == "save":
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            message_dialog(title="Success", text="บันทึกการตั้งค่าเรียบร้อยแล้ว!", style=style).run()
            break
        elif choice == "exit" or choice is None:
            if confirm(title="Exit", text="คุณแน่ใจหรือไม่ว่าต้องการออกโดยไม่บันทึก?", style=style).run():
                break

def manage_agents(data):
    agents = data["agents"]
    
    while True:
        agent_list = [(aid, f"{aid.upper()} ({'Enabled' if cfg.get('enabled') else 'Disabled'})") 
                      for aid, cfg in agents.items()]
        agent_list.append(("add", "➕ เพิ่ม Agent ใหม่"))
        agent_list.append(("back", "🔙 กลับเมนูหลัก"))

        choice = radiolist_dialog(
            title="Manage Agents",
            text="เลือก Agent ที่ต้องการแก้ไข:",
            values=agent_list,
            style=style
        ).run()

        if choice == "back" or choice is None:
            break
        elif choice == "add":
            aid = input_dialog(title="New Agent", text="ระบุชื่อ Agent ID (เช่น openai):", style=style).run()
            if aid:
                agents[aid.lower()] = {
                    "cmd": "",
                    "args": [],
                    "enabled": True,
                    "timeout": 180,
                    "color": "white",
                    "description": ""
                }
                edit_agent(agents[aid.lower()], aid.lower())
        else:
            action = radiolist_dialog(
                title=f"Agent: {choice}",
                text="เลือกสิ่งที่ต้องการทำ:",
                values=[
                    ("edit", "📝 แก้ไขการตั้งค่า"),
                    ("toggle", "Toggle Enabled/Disabled"),
                    ("delete", "🗑️ ลบ Agent"),
                    ("back", "🔙 กลับ")
                ],
                style=style
            ).run()

            if action == "edit":
                edit_agent(agents[choice], choice)
            elif action == "toggle":
                agents[choice]["enabled"] = not agents[choice].get("enabled", True)
            elif action == "delete":
                if confirm(title="Delete", text=f"คุณต้องการลบ {choice} ใช่หรือไม่?", style=style).run():
                    del agents[choice]
    
    return data

def edit_agent(cfg, aid):
    cfg["cmd"] = input_dialog(title=aid, text="Command/Path (เช่น qwen หรือ C:\\path\\to\\exe):", 
                              default=cfg.get("cmd", ""), style=style).run() or cfg["cmd"]
    
    args_str = input_dialog(title=aid, text="Arguments (แยกด้วยช่องว่าง เช่น -p --stream):", 
                            default=" ".join(cfg.get("args", [])), style=style).run()
    if args_str is not None:
        cfg["args"] = args_str.split()

    cfg["description"] = input_dialog(title=aid, text="คำอธิบาย (Description):", 
                                      default=cfg.get("description", ""), style=style).run() or cfg["description"]

def manage_settings(data):
    s = data["settings"]
    
    s["default_timeout"] = int(input_dialog(title="Settings", text="Default Timeout (วินาที):", 
                                            default=str(s.get("default_timeout", 180)), style=style).run() or s["default_timeout"])
    
    s["max_output_chars"] = int(input_dialog(title="Settings", text="Max Output Characters:", 
                                             default=str(s.get("max_output_chars", 10000)), style=style).run() or s["max_output_chars"])
    
    return data

if __name__ == "__main__":
    run_wizard()
