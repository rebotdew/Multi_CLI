# 🎮 Interactive CLI - สรุปวิธีใช้งาน

## ✅ สร้างเสร็จแล้ว!

Interactive CLI แบบใหม่ที่:
- ✅ เลือก agents ได้ (ทีละตัว หรือ หลายตัว)
- ✅ สั่งงานทีละตัว หรือ ทุกตัวพร้อมกัน
- ✅ ดูผลลัพธ์แบบ real-time
- ✅ รองรับภาษาไทย

---

## 🚀 เริ่มใช้งาน

### วิธีที่ 1: ใช้คำสั่ง (แนะนำ!)
```cmd
multi-ai-i
```

### วิธีที่ 2: ใช้ Python โดยตรง
```cmd
python C:\Users\user\multi-ai-agent\src\interactive.py
```

---

## 📋 คำสั่งที่ใช้ได้

### ข้อมูล
```
/help          - แสดงวิธีใช้
/agents        - ดู agents ทั้งหมด
/skills        - ดู skills ทั้งหมด
/clear         - ล้างหน้าจอ
/exit          - ออก
```

### เลือก Agents
```
/use qwen      - เลือก Qwen อย่างเดียว
/use codex,qwen - เลือก Codex + Qwen
/all           - ใช้ทุกตัว (codex, kimi, qwen, gemini)
/none          - ไม่เลือกตัวไหน
```

### สั่งงาน
```
สวัสดี         - ส่ง prompt ให้ agents ที่เลือก
/run code_review @file.py - รัน skill
/compare prompt - เปรียบเทียบผลลัพธ์
/consensus prompt - หา consensus
```

---

## 💡 ตัวอย่างการใช้งาน

### 1. เริ่ม Interactive Mode
```cmd
C:\> multi-ai-i

╔══════════════════════════════════════════════════════════════╗
║          🤖 Multi-Agent AI CLI - Interactive Mode         ║
║                                                              ║
║  codex │ kimi │ qwen │ gemini - เลือกใช้ตามต้องการ      ║
╚══════════════════════════════════════════════════════════════╝

📌 Active Agents: ไม่มี agents ที่เลือก (พิมพ์ /all เพื่อใช้ทุกตัว)
```

### 2. เลือก Agents
```
[no agents] ▶ /use qwen
✓ เลือก agents: qwen

📌 Active Agents: QWEN
```

### 3. ใช้ทุกตัวพร้อมกัน
```
[qwen] ▶ /all
✓ ใช้ทุก agents: codex, kimi, qwen, gemini

📌 Active Agents: CODEX, KIMI, QWEN, GEMINI
```

### 4. ส่ง Prompt
```
[codex,qwen] ▶ สวัสดี

⚡ Running on 2 agents: codex, qwen
────────────────────────────────────────────

✓ CODEX (25.3s)
────────────────────────────────────────────
Hello! How can I help you today?

✓ QWEN (10.5s)
────────────────────────────────────────────
สวัสดีครับ! มีอะไรให้ช่วยวันนี้?
```

### 5. รัน Skill
```
[codex,qwen] ▶ /run code_review @main.py

🎯 Running skill: code_review
   Agents: codex, qwen

✓ Skill: Code Review
Strategy: parallel_consensus | Duration: 35.8s

✓ CODEX (35.2s)
Found 3 issues...

✓ QWEN (34.9s)
พบปัญหา 3 จุด...

🤝 Consensus:
Both agents identified similar issues...
```

### 6. เปรียบเทียบ
```
[all] ▶ /compare วิธี terbaikในการ handle error

📊 Comparing 4 agents...

### ✓ CODEX (15.2s)
Use try-catch blocks...

### ✓ KIMI (45.3s)
ใช้ try-catch และ logging...

### ✓ QWEN (8.5s)
ใช้ error handling patterns...

### ✓ GEMINI (120.5s)
Implement comprehensive error handling...
```

---

## 🎯 Agents ที่มี

| Agent | ความเร็ว | แนะนำสำหรับ |
|-------|----------|------------|
| **qwen** | ⭐⭐⭐⭐⭐ (10s) | ใช้งานทั่วไป, เร็วสุด |
| **codex** | ⭐⭐⭐ (25-50s) | Code review, security |
| **kimi** | ⭐⭐ (50-80s) | Thai language, docs |
| **gemini** | ⭐ (100s+) | Complex tasks |

---

## 💡 เคล็ดลับ

### ใช้งานเร็ว (แนะนำ)
```
/use qwen
prompt...
```

### เปรียบเทียบ 2 agents
```
/use codex,qwen
prompt...
```

### หาคำตอบที่ดีที่สุด
```
/all
/consensus prompt...
```

### Code Review
```
/use codex,qwen
/run code_review @file.py
```

---

## 📊 สถานะ Agents ปัจจุบัน

```
/agents

🤖 Agents ทั้งหมด:
──────────────────────────────────────────────────
     CODEX | Timeout: 180s | ✓ พร้อม
      KIMI | Timeout: 180s | ✓ พร้อม
      QWEN | Timeout:  60s | ✓ พร้อม
    GEMINI | Timeout: 180s | ✓ พร้อม
```

---

## 🐛 Troubleshooting

### "ไม่มี agents ที่เลือก"
```
/all          # ใช้ทุกตัว
/use qwen     # เลือก Qwen
```

### "Agent ไม่พบ"
```
/agents       # ดู agents ที่มี
```

### ช้าเกินไป
```
/use qwen     # ใช้ Qwen เร็วสุด
```

---

## 🎉 พร้อมใช้งานแล้ว!

```cmd
multi-ai-i
```

แล้วพิมพ์:
```
/all
สวัสดี
```

---

**Created:** 2026-04-01
**Status:** ✅ Ready to Use
**Agents:** 4 (codex, kimi, qwen, gemini)
