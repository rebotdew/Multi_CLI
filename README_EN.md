# 🤖 Multi_CLI (Multi-Agent AI Assistant v2.0)

[🇺🇸 English | 🇹🇭 ภาษาไทย](README.md)

Run multiple AI CLI tools simultaneously (Codex, Kimi, Qwen, Gemini) with a powerful Skills and Orchestration system.

## ✨ Features (v2.0+)

- 🚀 **Modern TUI** - New Interactive interface (Style 3) with Command History and Auto-Suggest.
- 🪄 **Config Wizard** - Smart setup system (type `/setup`) to manage AI Agents without editing JSON files.
- 🧩 **Dynamic Plugins** - JSON-based Skills system in `src/skills/` for easy capability expansion.
- 🛡️ **Enhanced Security** - Strict Path Traversal and Command Injection protection.
- 🔄 **Multiple Strategies** - Parallel, Sequential, Consensus, Compare, Vote, Merge.
- 📊 **Smart Results** - Beautiful table summaries with automatic JSON result saving.
- 🧪 **CI/CD** - GitHub Actions for automated Linting and Testing on every push.

## 📦 Installation

### 1. Install Python 3.8+

```bash
python --version  # Must be 3.8 or higher
```

### 2. Install AI CLI Tools

Install the agents you want to use:

```bash
# OpenAI Codex
npm install -g @openai/codex

# Kimi CLI
uv tool install kimi-cli
# OR
pip install kimi-cli

# Qwen Code
npm install -g @qwen-code/qwen-code

# Google Gemini CLI
npm install -g @google/gemini-cli
```

### 3. Clone this project

```bash
git clone https://github.com/rebotdew/Multi_CLI.git
cd Multi_CLI
```

## 🚀 Quick Start

### Installation (One-time)

```bash
pip install -e .
```

### List Available Skills

```bash
ai list skills
```

### List Configured Agents

```bash
ai list agents
```

### Run a Skill (e.g., Code Review)

```bash
ai run code_review "@main.py"
```

### Run Prompt on All Agents

```bash
ai exec "Explain this code" --agents codex,kimi,qwen,gemini
```

### Generate Consensus

```bash
ai consensus "What is the best way to handle errors?"
```

## 📖 Commands

### `list` - Show items

```bash
# Show all skills
ai list skills

# Show agents
ai list agents
```

### `run` - Execute a skill

```bash
# Run code_review skill
ai run code_review "@src/main.py"

# Specify agents
ai run code_review "@src/main.py" --agents codex,gemini
```

### `config` - Manage configuration

```bash
# Show current config
ai config --show
```

## 🎯 Available Skills

| Skill | Description | Agents | Strategy |
|-------|-------------|--------|----------|
| `code_review` | Review code, find bugs and security issues | codex, qwen | parallel_consensus |
| `security_scan` | Security vulnerability analysis | codex, gemini | parallel_compare |
| `refactor` | Improve code structure | qwen, kimi | sequential |
| `test_generation` | Generate unit tests | codex, qwen, gemini | parallel_merge |
| `documentation` | Generate documentation | kimi, qwen, gemini | parallel |
| `bug_fix` | Find and fix bugs | codex, kimi, qwen, gemini | majority_vote |
| `translate_en` | Professional English translation | qwen, kimi, gemini | parallel_compare |

## 🪄 Interactive Wizard

Manage your agents and system settings easily without editing JSON files:

```bash
[Auto] ➜ /setup
```

## 📂 Project Structure

```
Multi_CLI/
├── src/
│   ├── skills/             # JSON Skill Plugins
│   ├── orchestrator.py     # Core logic
│   ├── smart_cli.py        # Modern TUI
│   └── config.json         # Configuration
├── output/                 # Saved results
└── README.md
```

## 📝 License

MIT License - Free to use.

## 🤝 Contributing

Welcome contributions! Feel free to create issues or PRs.

---

**Created with ❤️ for Multi-Agent AI Orchestration**
