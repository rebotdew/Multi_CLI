"""
skills_registry.py - Skills System
8 built-in skills พร้อม strategies
"""
import os
import json
from pathlib import Path
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
    def __init__(self, skills_dir: Optional[str] = None):
        self._skills: dict[str, Skill] = {}
        if skills_dir is None:
            self.skills_dir = Path(__file__).parent / "skills"
        else:
            self.skills_dir = Path(skills_dir)
        
        self.skills_dir.mkdir(exist_ok=True)
        self.load_all()

    def register(self, skill: Skill):
        self._skills[skill.key] = skill

    def get(self, key: str) -> Optional[Skill]:
        return self._skills.get(key)

    def list_all(self) -> list:
        return list(self._skills.values())

    def find_by_tag(self, tag: str) -> list:
        return [s for s in self._skills.values() if tag in s.tags]

    def load_all(self):
        """Load all .json skills from the skills directory"""
        for file in self.skills_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Convert strategy string to Enum
                    if "strategy" in data:
                        data["strategy"] = Strategy(data["strategy"])
                    
                    skill = Skill(**data)
                    self.register(skill)
            except Exception as e:
                print(f"Error loading skill from {file}: {e}")
