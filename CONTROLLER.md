# 🎮 AI CLI Controller - คู่มือการใช้งาน

## 🚀 เริ่มใช้งาน

```cmd
aic
```

หรือ

```cmd
ai-controller
```

---

## 💡 แนวคิด

**Controller** เป็น **ศูนย์กลาง** ที่:
1. รับคำสั่งจาก user
2. ตัดสินใจว่าจะส่งงานให้ agent ตัวไหน
3. ส่งงานให้ agents ที่เหมาะสม
4. รวบรวมผลลัพธ์มาแสดง

**ข้อดี:**
- ✅ User ไม่ต้องรู้ว่า agent ตัวไหนทำอะไร
- ✅ Controller เลือก agent ที่เหมาะสมให้อัตโนมัติ
- ✅ สั่งงานง่าย พิมพ์แค่ข้อความธรรมดา
- ✅ สามารถเลือก agent เฉพาะได้ถ้าต้องการ

---

## 📋 คำสั่งทั้งหมด

### ทั่วไป
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `/help` | แสดงวิธีใช้ |
| `/exit` | ออก |
| `/clear` | ล้างหน้าจอ |
| `/status` | ดูสถานะ agents |

### เลือก Agents
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `/use qwen` | เลือก Qwen |
| `/use codex,qwen` | เลือกหลายตัว |
| `/use all` | ใช้ทุกตัว |
| `/use none` | ไม่เลือก (auto) |

### สั่งงาน
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `ช่วยเขียนโค้ด` | ส่งให้ Controller จัดการ |
| `/to qwen สวัสดี` | ส่งไป qwen โดยตรง |
| `/broadcast สวัสดี` | ส่งให้ทุกตัว |
| `/run code_review @file` | รัน skill |

---

## 💡 ตัวอย่างการใช้งาน

### 1. เริ่ม Controller
```cmd
C:\> aic

╔══════════════════════════════════════════════════════════════╗
║          🎮 AI CLI Controller - Interactive Mode          ║
║                                                              ║
║  Controller รับคำสั่ง → ส่งงานให้ → kimi qwen gemini codex  ║
╚══════════════════════════════════════════════════════════════╝

📌 Active: ไม่ได้เลือก (พิมพ์ /use all)
```

### 2. Auto Mode (ไม่ต้องเลือก)
```
[auto] ▶ ช่วยเขียน Python function สำหรับคำนวณ factorial

📝 Documentation → Using KIMI

✓ KIMI (45.2s)
────────────────────────────────────────────
นี่คือ function สำหรับคำนวณ factorial:

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

### 3. เลือก Agent เฉพาะ
```
[auto] ▶ /use qwen
✓ เลือก: qwen

[qwen] ▶ อธิบาย list comprehension

⚡ Using selected agents: qwen

✓ QWEN (10.5s)
────────────────────────────────────────────
List comprehension คือ...
```

### 4. ส่งไป Agent เฉพาะ
```
[auto] ▶ /to codex review โค้ดนี้หน่อย

➤ Sending to CODEX...

✓ CODEX (25.3s)
────────────────────────────────────────────
Found 2 issues in the code...
```

### 5. Broadcast ไปทุกตัว
```
[auto] ▶ /broadcast สวัสดี

📢 Broadcasting to all agents...

✓ CODEX (15.2s) - Hello!
✓ KIMI (45.3s) - สวัสดีครับ
✓ QWEN (10.5s) - สวัสดีครับ
✓ GEMINI (120.5s) - Hi there!
```

### 6. รัน Skill
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

## 🤖 การเลือก Agent อัตโนมัติ

Controller จะวิเคราะห์ข้อความและเลือก agent ที่เหมาะสม:

| ประเภทงาน | Agent ที่เลือก | เหตุผล |
|-----------|---------------|--------|
| งานโค้ด | Codex + Qwen | เก่งโค้ด |
| งานเอกสาร | Kimi | เก่งภาษาไทย |
| งานเร็ว | Qwen | เร็วสุด |
| ทั่วไป | Qwen | สมดุล |

---

## 🎯 Agents ที่มี

| Agent | สถานะ | ความเร็ว | เหมาะสำหรับ |
|-------|-------|----------|------------|
| **qwen** | ✅ | ~10-40s | ทั่วไป, เร็ว |
| **codex** | ⚠️ | ~15-25s | Code review |
| **kimi** | ⚠️ | ~45-80s | ภาษาไทย, docs |
| **gemini** | ⚠️ | >120s | งานซับซ้อน |

---

## 💡 เคล็ดลับ

### ใช้งานทั่วไป (แนะนำ)
```
aic
<พิมพ์ข้อความ>
```

### ต้องการเร็ว
```
aic
/use qwen
<prompt>
```

### Code Review
```
aic
/run code_review @file.py
```

### เปรียบเทียบ
```
aic
/use codex,qwen
<prompt>
```

---

## 📁 โครงสร้างโปรเจค

```
multi-ai-agent/
├── src/
│   ├── controller.py       # ⭐ Controller ใหม่
│   ├── interactive.py      # Interactive Mode
│   ├── cli.py              # Command Mode
│   ├── orchestrator.py     # Core Logic
│   ├── skills_registry.py  # Skills
│   └── config.json         # Config
├── aic.bat                 # Controller Launcher
└── README.md               # คู่มือ
```

---

## 🐛 Troubleshooting

### "Command not found"
```cmd
python C:\Users\user\multi-ai-agent\src\controller.py
```

### "Agent ไม่พบ"
```cmd
/status    # ดู agents ที่มี
```

### ช้าเกินไป
```cmd
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
**Mode:** Controller-based Orchestration
