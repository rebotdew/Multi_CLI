# 🚀 Multi-Agent AI CLI - วิธีใช้งาน

## ✅ ติดตั้งเสร็จแล้ว!

---

## 📱 มี 2 Mode ให้ใช้งาน

### 1️⃣ **Command Mode** (พิมพ์คำสั่งแล้วจบ)

```cmd
multi-ai <command> [options]
```

**ตัวอย่าง:**
```cmd
multi-ai list skills
multi-ai exec "สวัสดี"
multi-ai run code_review "@main.py"
```

### 2️⃣ **Interactive Mode** (นั่งคุยต่อเนื่อง)

```cmd
multi-ai-interactive
```

**ตัวอย่าง:**
```cmd
C:\> multi-ai-interactive

[kimi] ▶ /help
[kimi] ▶ สวัสดี
[kimi] ▶ /run code_review ตรวจสอบโค้ดนี้
[kimi] ▶ /exit
```

---

## 🎯 เปรียบเทียบ 2 Mode

| Feature | Command Mode | Interactive Mode |
|---------|--------------|------------------|
| **ใช้งาน** | `multi-ai` | `multi-ai-interactive` |
| **เหมาะสำหรับ** | Script, Automation | คุยต่อเนื่อง, Explore |
| **Session** | ครั้งเดียว | ต่อเนื่อง |
| **Context** | ไม่จำ | จำบริบท |

---

## 📋 คำสั่งทั้งหมด (Command Mode)

### ดูข้อมูล
```cmd
multi-ai list skills          # ดู skills ทั้งหมด
multi-ai list agents          # ดู agents
multi-ai config --show        # ดู config
```

### รันงาน
```cmd
multi-ai run code_review "@file.py"     # รัน skill
multi-ai exec "prompt"                  # รัน prompt
multi-ai consensus "question"           # หา consensus
multi-ai compare "prompt"               # เปรียบเทียบ
```

---

## 📋 คำสั่งทั้งหมด (Interactive Mode)

```cmd
multi-ai-interactive
```

**ใน Interactive Mode:**
```
/help              - แสดงวิธีใช้
/exit              - ออก
/agents            - ดู agents
/skills            - ดู skills
/agent <name>      - เลือก agent
/all               - ใช้ทุก agent
/run <skill>       - รัน skill
/compare <prompt>  - เปรียบเทียบ
```

---

## 🤖 Agents ที่รองรับ

| Agent | สถานะ | ติดตั้งแล้ว |
|-------|-------|------------|
| **kimi** | ✅ พร้อมใช้ | ✅ v1.6 |
| codex | ❌ ปิด | ❌ |
| qwen | ❌ ปิด | ❌ |
| gemini | ❌ ปิด | ❌ |

**เปิดใช้ agent อื่น:** แก้ `src/config.json` ให้ `enabled: true`

---

## 🎯 Skills ที่มี

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

## 💡 ตัวอย่างการใช้งาน

### Command Mode

```cmd
# 1. ดู skills
multi-ai list skills

# 2. รัน prompt
multi-ai exec "สวัสดี"

# 3. รัน skill
multi-ai run documentation "เขียน docs สำหรับ hello()"

# 4. เปรียบเทียบ
multi-ai compare "วิธี optimize Python"
```

### Interactive Mode

```cmd
# 1. เริ่ม
multi-ai-interactive

# 2. ใน mode
[kimi] ▶ /help
[kimi] ▶ สวัสดี
[kimi] ▶ /run code_review ตรวจสอบโค้ด
[kimi] ▶ /compare วิธี handle error
[kimi] ▶ /exit
```

---

## 📁 ไฟล์ในโปรเจค

```
multi-ai-agent/
├── src/
│   ├── cli.py              # Command Mode
│   ├── orchestrator.py     # Core Logic
│   ├── skills_registry.py  # Skills
│   ├── interactive.py      # Interactive Mode ⭐ ใหม่!
│   └── config.json         # Config
├── output/                 # ผลลัพธ์
├── logs/                   # Logs
├── README.md               # คู่มือหลัก
├── INTERACTIVE.md          # คู่มือ Interactive
└── USAGE.md                # ไฟล์นี้
```

---

## 🎨 แนะนำการใช้งาน

### สำหรับใช้งานทั่วไป
```cmd
multi-ai-interactive        # นั่งคุยต่อเนื่อง
```

### สำหรับ Script/Automation
```cmd
multi-ai exec "prompt"      # รันแล้วจบ
```

### สำหรับ Compare
```cmd
multi-ai-interactive
/compare วิธี handle error  # เปรียบเทียบหลาย agent
```

---

## 🐛 Troubleshooting

### "Command not found"
```cmd
# ใช้ Python โดยตรง
python C:\Users\user\multi-ai-agent\src\cli.py list skills
python C:\Users\user\multi-ai-agent\src\interactive.py
```

### "No agents available"
เช็ค `src/config.json`:
```json
"kimi": {"enabled": true}
```

### Output แสดงไม่ครบ
```cmd
multi-ai exec "prompt" --verbose
```

---

## 🎉 พร้อมใช้งาน!

**เริ่มเลย:**
```cmd
multi-ai-interactive
```

หรือ

```cmd
multi-ai list skills
```

---

**Created:** 2026-03-31
**Version:** 1.0.0
**Status:** ✅ Ready to Use
