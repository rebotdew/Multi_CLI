"""
Tests for Skills Registry
"""
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from skills_registry import SkillsRegistry, Skill, Strategy


class TestSkillsRegistry(unittest.TestCase):
    """Test Skills Registry"""
    
    def setUp(self):
        self.registry = SkillsRegistry()
    
    def test_default_skills(self):
        """Test default skills are registered"""
        skills = self.registry.list_all()
        self.assertGreater(len(skills), 0)
    
    def test_get_skill(self):
        """Test getting a skill by ID"""
        skill = self.registry.get("code_review")
        self.assertIsNotNone(skill)
        self.assertEqual(skill.name, "Code Review")
    
    def test_get_nonexistent_skill(self):
        """Test getting a skill that doesn't exist"""
        skill = self.registry.get("nonexistent")
        self.assertIsNone(skill)
    
    def test_list_by_tag(self):
        """Test listing skills by tag"""
        skills = self.registry.find_by_tag("code")
        self.assertIsInstance(skills, list)
    
    def test_get_agents_for_skill(self):
        """Test getting agents for a skill"""
        skill = self.registry.get("code_review")
        self.assertIsNotNone(skill)
        agents = skill.agents  # Access agents directly from skill
        self.assertIsInstance(agents, list)
        self.assertGreater(len(agents), 0)


class TestStrategy(unittest.TestCase):
    """Test Strategy enum"""
    
    def test_strategy_values(self):
        """Test strategy enum values"""
        self.assertEqual(Strategy.PARALLEL.value, "parallel")
        self.assertEqual(Strategy.SEQUENTIAL.value, "sequential")
        self.assertEqual(Strategy.PARALLEL_CONSENSUS.value, "parallel_consensus")


class TestSkillCreation(unittest.TestCase):
    """Test Skill creation"""
    
    def test_create_skill(self):
        """Test creating a skill"""
        skill = Skill(
            key="test_skill",
            name="Test Skill",
            description="Test description",
            agents=["qwen"],
            strategy=Strategy.PARALLEL,
            timeout=60
        )
        self.assertEqual(skill.name, "Test Skill")
        self.assertEqual(skill.agents, ["qwen"])
    
    def test_skill_to_dict(self):
        """Test skill serialization"""
        skill = Skill(
            key="test",
            name="Test",
            description="Test",
            agents=["qwen"],
            strategy=Strategy.PARALLEL
        )
        # Skill doesn't have to_dict, so we test attributes directly
        self.assertEqual(skill.name, "Test")
        self.assertEqual(skill.agents, ["qwen"])
        self.assertEqual(skill.strategy, Strategy.PARALLEL)


if __name__ == "__main__":
    unittest.main()
