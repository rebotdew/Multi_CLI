"""
utils.py - Common UI Utilities
รวมฟังก์ชันที่ใช้ร่วมกันเพื่อลดความซ้ำซ้อนของโค้ด
"""
import os
import unicodedata
from orchestrator import C

def get_visual_width(text):
    """คำนวณความกว้างที่แท้จริงบนหน้าจอ (รองรับภาษาไทยและ Emoji)"""
    width = 0
    for char in text:
        # สระและวรรณยุกต์ไทย (ไม่กินพื้นที่)
        if 0x0E31 <= ord(char) <= 0x0E3A or 0x0E47 <= ord(char) <= 0x0E4E:
            continue
        # ตัวอักษรความกว้างเต็ม (Emoji, CJK)
        if unicodedata.east_asian_width(char) in ('W', 'F'):
            width += 2
        else:
            width += 1
    return width

def print_header(title="✨ MULTI-AI ASSISTANT (v2.0)", 
                 subtitle="พิมพ์ข้อความเพื่อถาม | /run <skill> | /help เพื่อดูคำสั่งทั้งหมด"):
    """แสดง Header รูปแบบ Style C (Gradient Divider) ที่เป็นมาตรฐานเดียวกัน"""
    os.system("cls" if os.name == "nt" else "clear")
    line_width = 68
    divider = "═" * line_width
    
    print(f"\n{C.CYAN}{divider}")
    print(f"{C.BOLD}  {title}{C.RESET}")
    print(f"{C.DIM}  {subtitle}{C.RESET}")
    print(f"{C.CYAN}{divider}{C.RESET}\n")
