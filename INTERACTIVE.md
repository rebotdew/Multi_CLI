# 🎮 Interactive CLI - คู่มือการใช้งาน

## 🚀 เริ่มใช้งาน

```cmd
multi-ai-i
```

หรือ

```cmd
python C:\Users\user\multi-ai-agent\src\interactive.py
```

---

## 📋 คำสั่งทั้งหมด

### ข้อมูลพื้นฐาน
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `/help` | แสดงวิธีใช้ |
| `/exit`, `/quit` | ออก |
| `/clear` | ล้างหน้าจอ |
| `/agents` | แสดง agents ทั้งหมด + สถานะ |
| `/skills` | แสดง skills ทั้งหมด |

### การเลือก Agents
| คำสั่ง | คำอธิบาย | ตัวอย่าง |
|--------|----------|----------|
| `/use <agent>` | เลือก agent เดียว | `/use qwen` |
| `/use <a1>,<a2>` | เลือกหลาย agents | `/use codex,qwen` |
| `/all` | ใช้ทุก agents พร้อมกัน | `/all` |
| `/none` | ไม่เลือก agent เลย | `/none` |

### การสั่งงาน
| คำสั่ง | คำอธิบาย |
|--------|----------|
| `/run <skill> <prompt>` | รัน skill |
| `/compare <prompt>` | เปรียบเทียบผลลัพธ์จากทุก agents |
| `/consensus <prompt>` | หา consensus จากทุก agents |

### ส่ง Prompt ธรรมดา
พิมพ์ข้อความแล้วกด Enter - ส่งให้ agents ที่เลือก

---

## 💡 ตัวอย่างการใช้งาน

### 1. เริ่ม Interactive Mode
```cmd
C:\> multi-ai-i

╔══════════════════════════════════════════════════════════════╗
║          🤖 Multi-Agent AI CLI - Interactive Mode         ║
║                                                              ║
║  codex │ kimi │ qwen │ gemini - เลือกใช้ตามต้องการ      ║
║                                                              ║
║  พิมพ์ /help เพื่อดูคำสั่งทั้งหมด                  ║
║  พิมพ์ /exit เพื่อออก                                   ║
╚══════════════════════════════════════════════════════════════╝

📌 Active Agents: ไม่มี agents ที่เลือก (พิมพ์ /all เพื่อใช้ทุกตัว)
```

### 2. เลือก Agents
```
[no agents] ▶ /use qwen
✓ เลือก agents: qwen

📌 Active Agents: QWEN

[qwen] ▶ /all
✓ ใช้ทุก agents: codex, kimi, qwen, gemini

📌 Active Agents: CODEX, KIMI, QWEN, GEMINI
```

### 3. ส่ง Prompt
```
[qwen] ▶ สวัสดี

✓ QWEN (10.2s)
────────────────────────────────────────────
สวัสดีครับ! มีอะไรให้ช่วยวันนี้?
```

### 4. ใช้หลาย Agents พร้อมกัน
```
[codex,qwen] ▶ อธิบาย Python list comprehension

⚡ Running on 2 agents: codex, qwen
────────────────────────────────────────────

✓ CODEX (25.3s)
────────────────────────────────────────────
List comprehension is a concise way to create lists...

✓ QWEN (10.5s)
────────────────────────────────────────────
Python list comprehension คือวิธีสร้าง list แบบสั้น...
```

### 5. รัน Skill
```
[codex,qwen] ▶ /run code_review @main.py

🎯 Running skill: code_review
   Agents: codex, qwen

✓ Skill: Code Review
Strategy: parallel_consensus | Duration: 35.8s

✓ CODEX (35.2s)
────────────────────────────────────────────
Found 3 issues in the code...

✓ QWEN (34.9s)
────────────────────────────────────────────
พบปัญหา 3 จุดในโค้ด...

🤝 Consensus:
────────────────────────────────────────────
Both agents identified similar issues...
```

### 6. เปรียบเทียบ
```
[all] ▶ /compare วิธี terbaikในการ handle error

📊 Comparing 4 agents...

## Agent Comparison

### ✓ CODEX
**Duration:** 15.2s
Use try-catch blocks...

### ✓ KIMI
**Duration:** 45.3s
ใช้ try-catch และ logging...

### ✓ QWEN
**Duration:** 8.5s
ใช้ error handling patterns...

### ✓ GEMINI
**Duration:** 120.5s
Implement comprehensive error handling...
```

### 7. หา Consensus
```
[all] ▶ /consensus ควรใช้ Python หรือ Go สำหรับ web API?

🤝 Generating consensus from 4 agents...

📊 Results:
✓ CODEX (20.1s) - Python is better for...
✓ KIMI (55.2s) - ขึ้นอยู่กับ use case...
✓ QWEN (9.3s) - Both have pros and cons...
✓ GEMINI (130.5s) - Consider these factors...

🤝 Consensus:
────────────────────────────────────────────
Based on all responses, the consensus is:
- Use Python for rapid development...
- Use Go for high performance...
```

---

## 🎯 Skills ที่มี

| Skill | คำอธิบาย | Agents ที่แนะนำ |
|-------|----------|----------------|
| `code_review` | Review code หา bugs | codex, qwen |
| `security_scan` | Security audit | codex, gemini |
| `refactor` | ปรับปรุง code | qwen, kimi |
| `test_generation` | สร้าง tests | codex, qwen, gemini |
| `documentation` | เขียน docs | kimi, qwen, gemini |
| `bug_fix` | แก้ bugs | codex, kimi, qwen, gemini |
| `performance` | Optimize | codex, gemini |
| `architecture` | Review architecture | codex, qwen, gemini |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | คำอธิบาย |
|----------|----------|
| `Ctrl+C` | ยกเลิกคำสั่งปัจจุบัน |
| `Ctrl+D` | ออก (บนบรรทัดว่าง) |
| `↑/↓` | ประวัติคำสั่ง |

---

## 💡 เคล็ดลับการใช้งาน

### ใช้งานเร็ว (แนะนำ Qwen)
```
/agent qwen
prompt...
```

### เปรียบเทียบ 2 agents (สมดุล)
```
/agent codex,qwen
prompt...
```

### หาคำตอบที่ดีที่สุด (Consensus)
```
/all
/consensus prompt...
```

### Code Review
```
/agent codex,qwen
/run code_review @file.py
```

---

## 🐛 Troubleshooting

### "ไม่มี agents ที่เลือก"
```
/all          # ใช้ทุกตัว
/use qwen     # เลือก Qwen
```

### "Agent ไม่พบ"
เช็คชื่อ agents ที่มี:
```
/agents
```

### Output แสดงไม่ครบ
ผลลัพธ์ยาวเกิน 1500 ตัวจะถูกตัด
ดูไฟล์เต็มใน `output/` folder

---

## 📁 โครงสร้างโปรเจค

```
multi-ai-agent/
├── src/
│   ├── interactive.py      # Interactive CLI ⭐
│   ├── cli.py              # Command Mode
│   ├── orchestrator.py     # Core Logic
│   ├── skills_registry.py  # Skills
│   └── config.json         # Config
├── output/                 # ผลลัพธ์ที่บันทึก
├── logs/                   # Log files
└── README.md               # คู่มือ
```

---

**พร้อมใช้งานแล้ว!** 🎉
