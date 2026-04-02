# 🎮 Central Control Agent CLI (AIC)

ศูนย์กลางควบคุม AI CLI ทั้งหมด (Kimi, Codex, Qwen, Gemini) ในที่เดียว

---

## 🚀 เริ่มใช้งาน

```cmd
aic
```

หรือ

```cmd
ai-controller
```

---

## 📋 คำสั่งทั้งหมด

### 🔧 ทั่วไป
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `/help` | แสดงวิธีใช้ |
| `/exit` หรือ `/quit` | ออกจากโปรแกรม |
| `/clear` | ล้างหน้าจอ |
| `/status` | ดูสถานะ agents |

### 🤖 เลือก Agents
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `/use <agent>` | เลือก agent (เช่น `/use qwen`) |
| `/use <agent1>,<agent2>` | เลือกหลาย agents (เช่น `/use codex,qwen`) |
| `/use all` | ใช้ทุก agent |
| `/use none` | ยกเลิกการเลือก (auto mode) |

### 💬 ส่งข้อความ
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `<ข้อความ>` | ส่งให้ agent ที่เลือก หรือ auto-route |
| `/to <agent> <ข้อความ>` | ส่งไป agent เฉพาะ |
| `/broadcast <ข้อความ>` | ส่งให้ทุก agent |

### 🎯 รัน Skills
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `/run <skill> [ข้อความ]` | รัน skill (เช่น `/run code_review @file.py`) |
| `/skills` | ดู skills ทั้งหมด |

---

## 💡 ตัวอย่างการใช้งาน

### 1. เริ่มต้น (Auto Mode)
```
C:\> aic

==============================================================
AI CLI Controller - Interactive Mode
Controller routes prompts to configured AI CLIs.
Type /help for commands, /exit to quit.
==============================================================

Active: none selected (/use all)

[auto] ▶ ช่วยเขียน Python function คำนวณ factorial

📝 Auto-routing → Using QWEN

✓ QWEN (12.5s)
------------------------------------------------------------
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

### 2. เลือก Agent เฉพาะ
```
[auto] ▶ /use qwen
✓ Selected: qwen

[qwen] ▶ อธิบาย list comprehension

✓ QWEN (8.2s)
------------------------------------------------------------
List comprehension คือวิธีสร้าง list ใหม่จาก list เดิม...
```

### 3. ส่งไป Agent เฉพาะ
```
[auto] ▶ /to codex review โค้ดนี้หน่อย

➤ Sending to CODEX...

✓ CODEX (22.3s)
------------------------------------------------------------
Found 2 issues in the code...
```

### 4. Broadcast ไปทุกตัว
```
[auto] ▶ /broadcast สวัสดี

📢 Broadcasting to all agents...

✓ CODEX (15.2s) - Hello! How can I help?
✓ KIMI (45.3s) - สวัสดีครับ มีอะไรให้ช่วยไหมครับ
✓ QWEN (10.5s) - สวัสดีครับ
✓ GEMINI (120.5s) - Hi there!
```

### 5. รัน Skill
```
[auto] ▶ /run code_review @main.py

🎯 Running skill: code_review

✓ Skill: Code Review
Strategy: parallel_consensus | Duration: 35.8s

✓ CODEX (35.2s)
Found 3 issues...

✓ QWEN (34.9s)
พบปัญหา 3 จุด...

🤝 Consensus:
Both agents identified similar issues...
```

---

## 🤖 Agents ที่รองรับ

| Agent | สี | ความเร็ว | เหมาะสำหรับ |
|-------|-----|----------|------------|
| **kimi** | 🟡 เหลือง | ~45-80s | ภาษาไทย, docs |
| **codex** | 🟢 เขียว | ~15-25s | Code review |
| **qwen** | 🟣 ม่วง | ~10-40s | เร็ว, ทั่วไป |
| **gemini** | 🔵 น้ำเงิน | >120s | งานซับซ้อน |

---

## 🎯 Auto-Routing (ไม่ต้องเลือก Agent)

Controller จะวิเคราะห์ข้อความและเลือก agent อัตโนมัติ:

| ประเภทงาน | คำสัญญาณ | Agent ที่เลือก |
|-----------|----------|----------------|
| งานเร็ว | "quick", "fast" | Qwen |
| งานโค้ด | "code", "function", "review" | Codex + Qwen |
| งานเอกสาร | "doc", "explain" | Kimi |
| ทั่วไป | - | Qwen |

---

## 📁 Skills ที่มี

| Skill | คำอธิบาย |
|-------|----------|
| `code_review` | Review code หา bugs |
| `security_scan` | Security audit |
| `refactor` | ปรับปรุง code |
| `test_generation` | สร้าง tests |
| `documentation` | เขียน docs |
| `bug_fix` | แก้ bugs |
| `performance` | Optimize |
| `architecture` | Review architecture |

---

## 🔧 ไฟล์ที่เกี่ยวข้อง

```
multi-ai-agent/
├── aic.bat              # ⭐ Central Controller (shortcut)
├── ai-controller.bat    # Controller launcher
├── src/
│   ├── controller.py    # Controller logic
│   ├── orchestrator.py  # Core orchestration
│   ├── skills_registry.py # Skills
│   └── config.json      # Agent config
└── CENTRAL_CONTROLLER.md # คู่มือนี้
```

---

## 🐛 แก้ไขปัญหา

### "Command not found"
```cmd
# ใช้ Python โดยตรง
python C:\Users\user\multi-ai-agent\src\controller.py
```

### "No agents available"
```cmd
# ตรวจสอบ config
aic
/status
```

### Agent ช้าเกินไป
```cmd
aic
/use qwen  # ใช้ Qwen เร็วสุด
```

---

## 🎉 พร้อมใช้งาน!

```cmd
aic
```

แล้วพิมพ์:
```
ช่วยเขียนโค้ด Python สำหรับคำนวณ factorial
```

---

**Created:** 2026-04-01
**Status:** ✅ Ready to Use
**Version:** 1.0.0
