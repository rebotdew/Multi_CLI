# 🤖 Multi_CLI (Multi-Agent AI Assistant v2.0)

รัน AI CLI tools หลายตัวพร้อมกัน (Codex, Kimi, Qwen, Gemini) ด้วยระบบ Skills และ Orchestration

## ✨ Features

- 🚀 **รันพร้อมกัน** - รัน 4 AI agents พร้อมกันแบบ parallel
- 🎯 **Skills System** - ใช้ skills สำเร็จรูปสำหรับงานต่างๆ
- 🔄 **Multiple Strategies** - Parallel, Sequential, Consensus, Compare, Vote
- 📊 **เปรียบเทียบผลลัพธ์** - ดูความแตกต่างระหว่าง agents
- 💾 **บันทึกผลลัพธ์** - เก็บผลลัพธ์เป็น JSON โดยอัตโนมัติ
- 🎨 **สีสวยๆ** - Terminal output ที่มีสีสัน อ่านง่าย

## 📦 Installation

### 1. ติดตั้ง Python 3.8+

```bash
python --version  # ต้องเป็น 3.8 ขึ้นไป
```

### 2. ติดตั้ง AI CLI Tools

เลือกติดตั้งตามที่ต้องการ:

```bash
# OpenAI Codex
npm install -g @openai/codex

# Kimi CLI
uv tool install kimi-cli
# หรือ
pip install kimi-cli

# Qwen Code
npm install -g @qwen-code/qwen-code

# Google Gemini CLI
npm install -g @google/gemini-cli
```

### 3. Clone โปรเจคนี้

```bash
cd multi-ai-agent
```

## 🚀 Quick Start

### ติดตั้ง (ครั้งเดียว)

```bash
cd multi-ai-agent
pip install -e .
```

### ดู Skills ที่มี

```bash
multi-ai list skills
# หรือ
maai list skills
```

### ดู Agents ที่ config ไว้

```bash
multi-ai list agents
```

### รัน Skill (Code Review)

```bash
multi-ai run code_review "@main.py"
```

### รัน Prompt บนทุก Agents พร้อมกัน

```bash
multi-ai exec "อธิบายโค้ดนี้" --agents codex,kimi,qwen,gemini
```

### สร้าง Consensus จากหลาย Agents

```bash
multi-ai consensus "วิธี terbaikในการ handle error คืออะไร?"
```

### เปรียบเทียบผลลัพธ์

```bash
multi-ai compare "Review โค้ดนี้" --agents codex,gemini
```

## 📖 Commands

### `list` - แสดงรายการ

```bash
# แสดง skills ทั้งหมด
python src/cli.py list skills

# แสดง agents
python src/cli.py list agents
```

### `run` - รัน skill

```bash
# รัน skill code_review
python src/cli.py run code_review "@src/main.py"

# รัน skill security_scan
python src/cli.py run security_scan "@src/auth.py"

# ระบุ agents เฉพาะ
python src/cli.py run code_review "@src/main.py" --agents codex,gemini
```

### `exec` - รัน prompt โดยตรง

```bash
# รันพร้อมกัน (default)
python src/cli.py exec "อธิบายฟังก์ชันนี้" --parallel

# รันตามลำดับ
python src/cli.py exec "อธิบายฟังก์ชันนี้" --sequential

# แสดงผลลัพธ์เต็มๆ
python src/cli.py exec "อธิบายฟังก์ชันนี้" --verbose
```

### `consensus` - สร้างฉันทามติ

```bash
# ให้ AI สรุป consensus จากทุกตัว
python src/cli.py consensus "Best practice สำหรับ error handling คืออะไร?"
```

### `compare` - เปรียบเทียบ

```bash
# เปรียบเทียบผลลัพธ์จากทุก agent
python src/cli.py compare "วิธี optimize โค้ดนี้?"
```

### `config` - จัดการ config

```bash
# แสดง config ปัจจุบัน
python src/cli.py config --show

# สร้าง config ใหม่
python src/cli.py config --create
```

## 🎯 Available Skills

| Skill | Description | Agents | Strategy |
|-------|-------------|--------|----------|
| `code_review` | Review code, หา bugs และ security issues | codex, kimi, qwen, gemini | parallel_consensus |
| `security_scan` | Security vulnerability analysis | codex, gemini | parallel_compare |
| `refactor` | Refactor code ให้ดีขึ้น | qwen, kimi | sequential |
| `test_generation` | Generate unit tests | codex, qwen, gemini | parallel_merge |
| `documentation` | Generate documentation | kimi, qwen, gemini | parallel |
| `bug_fix` | Find and fix bugs | codex, kimi, qwen, gemini | majority_vote |
| `performance` | Optimize performance | codex, gemini | parallel_compare |
| `architecture` | Review architecture | codex, qwen, gemini | parallel_consensus |

## ⚙️ Configuration

แก้ไขไฟล์ `src/config.json`:

```json
{
  "agents": {
    "codex": {
      "cmd": "codex",
      "args": ["-p"],
      "timeout": 120,
      "enabled": true,
      "env_vars": {
        "OPENAI_API_KEY": "your-key-here"
      }
    }
  },
  "settings": {
    "default_timeout": 120,
    "max_retries": 2,
    "save_outputs": true
  }
}
```

### Environment Variables

แต่ละ CLI อาจต้องการ API keys:

```bash
# Codex
export OPENAI_API_KEY="your-key"

# Kimi
export KIMI_API_KEY="your-key"

# Qwen
export DASHSCOPE_API_KEY="your-key"

# Gemini
export GEMINI_API_KEY="your-key"
```

## 📂 Project Structure

```
multi-ai-agent/
├── src/
│   ├── cli.py              # CLI interface
│   ├── orchestrator.py     # Core orchestration logic
│   ├── skills_registry.py  # Skills definitions
│   └── config.json         # Configuration
├── output/                 # Saved results
├── logs/                   # Log files
└── README.md
```

## 💡 Usage Examples

### 1. Code Review แบบเร็ว

```bash
python src/cli.py run code_review "@src/main.py" --verbose
```

### 2. Security Scan ก่อน Deploy

```bash
python src/cli.py run security_scan "@src/" --agents codex,gemini
```

### 3. Generate Tests

```bash
python src/cli.py run test_generation "@src/calculator.py"
```

### 4. เปรียบเทียบ 4 Agents

```bash
python src/cli.py compare "อธิบาย React Hooks" --agents codex,kimi,qwen,gemini
```

### 5. หา Consensus

```bash
python src/cli.py consensus "ควรใช้ Python หรือ Go สำหรับ project นี้?"
```

## 🔧 Adding Custom Skills

แก้ไข `src/skills_registry.py`:

```python
self.register(Skill(
    name="My Custom Skill",
    description="Description here",
    agents=["codex", "qwen"],
    strategy=Strategy.PARALLEL,
    timeout=120,
    tags=["custom", "my-skill"],
    system_prompt="""You are an expert..."""
))
```

## 🐛 Troubleshooting

### "Command not found"

ติดตั้ง CLI ที่ขาด:
```bash
npm install -g @openai/codex
```

### "Timeout"

เพิ่ม timeout ใน config:
```json
"codex": {"timeout": 300}
```

### "No API key"

ตั้ง environment variables:
```bash
export OPENAI_API_KEY="your-key"
```

## 📝 License

MIT License - ใช้งานได้อิสระ

## 🤝 Contributing

Welcome contributions! สร้าง issue หรือ PR ได้เลย

---

**Created with ❤️ for Multi-Agent AI Orchestration**
