"""
skills_registry.py - Skills System
8 built-in skills พร้อม strategies
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class Strategy(str, Enum):
    PARALLEL            = "parallel"             # รันพร้อมกัน แสดงทุกผล
    SEQUENTIAL          = "sequential"           # รันตามลำดับ
    PARALLEL_CONSENSUS  = "parallel_consensus"   # รันพร้อมกัน + สรุป
    PARALLEL_COMPARE    = "parallel_compare"     # รันพร้อมกัน + เปรียบเทียบ
    PARALLEL_MERGE      = "parallel_merge"       # รันพร้อมกัน + รวมผล
    MAJORITY_VOTE       = "majority_vote"        # รันพร้อมกัน + โหวต
    SINGLE              = "single"               # รันตัวเดียว


@dataclass
class Skill:
    name: str
    key: str
    description: str
    agents: list
    strategy: Strategy
    timeout: int = 120
    tags: list = field(default_factory=list)
    system_prompt: str = ""

    def get_full_prompt(self, user_prompt: str) -> str:
        if self.system_prompt:
            return f"{self.system_prompt}\n\n{user_prompt}"
        return user_prompt


class SkillsRegistry:
    def __init__(self):
        self._skills: dict[str, Skill] = {}
        self._register_defaults()

    def register(self, skill: Skill):
        self._skills[skill.key] = skill

    def get(self, key: str) -> Optional[Skill]:
        return self._skills.get(key)

    def list_all(self) -> list:
        return list(self._skills.values())

    def find_by_tag(self, tag: str) -> list:
        return [s for s in self._skills.values() if tag in s.tags]

    def _register_defaults(self):
        self.register(Skill(
            key="code_review",
            name="Code Review",
            description="ตรวจสอบ code หา bugs, issues, และปัญหา",
            agents=["codex", "qwen"],
            strategy=Strategy.PARALLEL_CONSENSUS,
            timeout=120,
            tags=["code", "review", "quality"],
            system_prompt=(
                "You are an expert code reviewer. Analyze the following code carefully.\n"
                "Look for: bugs, security issues, performance problems, bad practices.\n"
                "Format your response with sections: Issues Found, Suggestions, Summary."
            ),
        ))

        self.register(Skill(
            key="security_scan",
            name="Security Scan",
            description="ตรวจหา security vulnerabilities",
            agents=["codex", "gemini"],
            strategy=Strategy.PARALLEL_COMPARE,
            timeout=150,
            tags=["security", "code", "audit"],
            system_prompt=(
                "You are a security expert. Perform a thorough security audit.\n"
                "Check for: SQL injection, XSS, authentication issues, data exposure,\n"
                "input validation, dependency vulnerabilities.\n"
                "Rate severity: CRITICAL / HIGH / MEDIUM / LOW."
            ),
        ))

        self.register(Skill(
            key="refactor",
            name="Refactor",
            description="ปรับปรุง code structure ให้ดีขึ้น",
            agents=["qwen", "kimi"],
            strategy=Strategy.SEQUENTIAL,
            timeout=120,
            tags=["code", "refactor", "improve"],
            system_prompt=(
                "You are a software architect. Refactor the following code:\n"
                "- Improve readability and maintainability\n"
                "- Apply SOLID principles where applicable\n"
                "- Remove code duplication\n"
                "- Provide the refactored code with explanations."
            ),
        ))

        self.register(Skill(
            key="test_generation",
            name="Test Generation",
            description="สร้าง unit tests อัตโนมัติ",
            agents=["codex", "qwen", "gemini"],
            strategy=Strategy.PARALLEL_MERGE,
            timeout=120,
            tags=["code", "testing", "quality"],
            system_prompt=(
                "You are a testing expert. Generate comprehensive unit tests for the following code.\n"
                "Include: happy path tests, edge cases, error cases.\n"
                "Use appropriate testing framework (pytest for Python, Jest for JS, etc.).\n"
                "Add clear test names and comments."
            ),
        ))

        self.register(Skill(
            key="documentation",
            name="Documentation",
            description="เขียน documentation อัตโนมัติ",
            agents=["kimi", "qwen", "gemini"],
            strategy=Strategy.PARALLEL,
            timeout=120,
            tags=["docs", "writing"],
            system_prompt=(
                "You are a technical writer. Create clear, comprehensive documentation.\n"
                "Include: overview, parameters/arguments, return values, examples, notes.\n"
                "Write in both Thai and English where appropriate."
            ),
        ))

        self.register(Skill(
            key="bug_fix",
            name="Bug Fix",
            description="หาและแก้ไข bugs",
            agents=["codex", "kimi", "qwen", "gemini"],
            strategy=Strategy.MAJORITY_VOTE,
            timeout=150,
            tags=["code", "debug", "fix"],
            system_prompt=(
                "You are a debugging expert. Analyze this code/error and:\n"
                "1. Identify the root cause of the bug\n"
                "2. Explain why it's happening\n"
                "3. Provide the fixed code\n"
                "4. Suggest how to prevent similar bugs."
            ),
        ))

        self.register(Skill(
            key="performance",
            name="Performance Optimization",
            description="วิเคราะห์และ optimize performance",
            agents=["codex", "gemini"],
            strategy=Strategy.PARALLEL_COMPARE,
            timeout=120,
            tags=["code", "performance", "optimize"],
            system_prompt=(
                "You are a performance engineer. Analyze and optimize this code:\n"
                "- Identify bottlenecks and inefficiencies\n"
                "- Suggest algorithmic improvements (time/space complexity)\n"
                "- Provide optimized version with benchmarks where possible."
            ),
        ))

        self.register(Skill(
            key="architecture",
            name="Architecture Review",
            description="Review system architecture และ design",
            agents=["codex", "qwen", "gemini"],
            strategy=Strategy.PARALLEL_CONSENSUS,
            timeout=150,
            tags=["architecture", "design", "review"],
            system_prompt=(
                "You are a software architect. Review this architecture/design:\n"
                "- Evaluate scalability, maintainability, reliability\n"
                "- Identify design patterns used and suggest improvements\n"
                "- Comment on coupling, cohesion, separation of concerns\n"
                "- Provide concrete recommendations."
            ),
        ))
