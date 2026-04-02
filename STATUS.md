# ✅ สรุปการใช้งาน Multi-Agent AI CLI

**อัพเดท:** 2026-04-01 11:26

---

## 🎯 สถานะ Agents

| Agent | สถานะ | เวลาตอบสนอง | หมายเหตุ |
|-------|-------|------------|----------|
| **qwen** | ✅ พร้อมใช้ | ~40s | เร็วสุดในตอนนี้ |
| **kimi** | ⚠️ ช้ามาก | >120s | มัก timeout |
| **codex** | ❌ ปิด | - | มีปัญหา config profile |
| **gemini** | ❌ ปิด | - | ช้ามาก |

---

## 🚀 วิธีใช้งาน

### Interactive Mode (แนะนำ!)

```cmd
multi-ai-i
```

**แล้วพิมพ์คำสั่ง:**
```
/use qwen           # เลือก Qwen
/all                # ใช้ทุกตัว
สวัสดี              # ส่ง prompt
/run code_review @file.py  # รัน skill
/exit               # ออก
```

### Command Mode

```cmd
# ใช้ Qwen
multi-ai exec "สวัสดี" --agents qwen

# รัน skill
multi-ai run code_review "@file.py" --agents qwen
```

---

## 💡 ตัวอย่าง Interactive Session

```cmd
C:\> multi-ai-i

╔══════════════════════════════════════════════════════════════╗
║          🤖 Multi-Agent AI CLI - Interactive Mode         ║
║                                                              ║
║  codex │ kimi │ qwen │ gemini - เลือกใช้ตามต้องการ      ║
╚══════════════════════════════════════════════════════════════╝

📌 Active Agents: ไม่มี agents ที่เลือก (พิมพ์ /all เพื่อใช้ทุกตัว)

[no agents] ▶ /use qwen
✓ เลือก agents: qwen

📌 Active Agents: QWEN

[qwen] ▶ สวัสดี

⚡ Running on 1 agents: qwen
────────────────────────────────────────────

✓ QWEN (39.68s)
────────────────────────────────────────────
Hello! How can I help you today?

[qwen] ▶ /exit
Goodbye! 👋
```

---

## 📋 คำสั่งทั้งหมด

### ข้อมูล
- `/help` - แสดงวิธีใช้
- `/agents` - ดู agents ทั้งหมด
- `/skills` - ดู skills ทั้งหมด
- `/clear` - ล้างหน้าจอ

### เลือก Agents
- `/use qwen` - เลือก Qwen
- `/use codex,qwen` - เลือกหลายตัว
- `/all` - ใช้ทุกตัว
- `/none` - ไม่เลือก

### สั่งงาน
- `สวัสดี` - ส่ง prompt (พิมพ์ปกติ)
- `/run code_review @file` - รัน skill
- `/compare prompt` - เปรียบเทียบ
- `/consensus prompt` - หา consensus

### ระบบ
- `/exit`, `/quit` - ออก

---

## 🎯 Skills ที่มี

1. `code_review` - Review code
2. `security_scan` - Security audit
3. `refactor` - Refactor code
4. `test_generation` - Generate tests
5. `documentation` - Write docs
6. `bug_fix` - Fix bugs
7. `performance` - Optimize
8. `architecture` - Architecture review

---

## ⚠️ ปัญหาที่พบ

### Codex Error
```
Error: config profile `xxx` not found
```
**แก้โดย:** ปิด Codex ชั่วคราว (enabled: false)

### Timeout
Kimi, Gemini ช้ามาก (>120s)
**แก้โดย:** ใช้ Qwen อย่างเดียว

### Echo ไม่ทำงาน
```cmd
echo สวัสดี | multi-ai-i  # ไม่ทำงาน
```
**แก้โดย:** ใช้ interactive mode แบบ manual

---

## 🔧 Config ปัจจุบัน

```json
{
  "agents": {
    "codex": {"enabled": false},
    "kimi": {"enabled": true, "timeout": 120},
    "qwen": {"enabled": true, "timeout": 60},
    "gemini": {"enabled": false}
  }
}
```

---

## 💡 เคล็ดลับ

### ใช้งานทั่วไป
```
multi-ai-i
/use qwen
<prompt>
```

### Code Review
```
multi-ai-i
/use qwen
/run code_review @file.py
```

### เปรียบเทียบ (ถ้าเปิดหลายตัว)
```
multi-ai-i
/all
/compare prompt
```

---

## 📁 ไฟล์สำคัญ

```
multi-ai-agent/
├── src/
│   ├── interactive.py      # Interactive CLI ⭐
│   ├── orchestrator.py     # Core logic
│   ├── skills_registry.py  # Skills
│   └── config.json         # Config
├── output/                 # Results
├── README.md               # คู่มือหลัก
├── INTERACTIVE_GUIDE.md    # Interactive guide
└── STATUS.md               # สถานะ
```

---

## 🎉 พร้อมใช้งาน!

```cmd
multi-ai-i
```

**แนะนำ:** ใช้ Qwen อย่างเดียว (เร็วสุด ~40s)

---

**Status:** ✅ Ready to Use (Qwen only recommended)
