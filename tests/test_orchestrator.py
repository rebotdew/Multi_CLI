"""
Tests for Orchestrator module
"""
import unittest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from orchestrator import Orchestrator, load_config, _validate_config, MAX_PROMPT_LENGTH


class TestConfigValidation(unittest.TestCase):
    """Test configuration validation"""
    
    def test_default_config(self):
        """Test default config is valid"""
        config = load_config()
        self.assertIn("agents", config)
        self.assertIn("settings", config)
    
    def test_missing_agents(self):
        """Test config with missing agents"""
        config = {"settings": {}}
        _validate_config(config)
        self.assertIn("agents", config)
    
    def test_missing_settings(self):
        """Test config with missing settings"""
        config = {"agents": {}}
        _validate_config(config)
        self.assertIn("settings", config)
    
    def test_invalid_timeout(self):
        """Test timeout validation"""
        config = {
            "agents": {"test": {"cmd": "test", "timeout": 1000}},
            "settings": {}
        }
        _validate_config(config)
        self.assertEqual(config["agents"]["test"]["timeout"], 60)


class TestPathValidation(unittest.TestCase):
    """Test path validation for security"""
    
    def setUp(self):
        self.orch = Orchestrator()
    
    def test_valid_path(self):
        """Test valid path is accepted"""
        # Create a temp file in current directory
        test_file = Path("test_file.txt")
        test_file.write_text("test")
        
        result = self.orch._validate_file_read(str(test_file))
        self.assertTrue(result)
        
        # Cleanup
        test_file.unlink()
    
    def test_path_traversal_blocked(self):
        """Test path traversal is blocked"""
        # This should be blocked (going outside current directory)
        result = self.orch._validate_path("../etc/passwd")
        self.assertFalse(result)
    
    def test_allowed_extensions(self):
        """Test allowed file extensions"""
        valid_files = [
            "test.txt",
            "code.py",
            "script.js",
            "README.md",
            "config.json"
        ]
        for fname in valid_files:
            ext = Path(fname).suffix
            self.assertIn(ext, self.orch.ALLOWED_FILE_EXTENSIONS 
                         if hasattr(self.orch, 'ALLOWED_FILE_EXTENSIONS') 
                         else ['.txt', '.py', '.js', '.md', '.json'])


class TestPromptValidation(unittest.TestCase):
    """Test prompt validation"""
    
    def setUp(self):
        self.orch = Orchestrator()
    
    def test_short_prompt(self):
        """Test short prompt is accepted"""
        result = self.orch._validate_prompt("Hello")
        self.assertTrue(result)
    
    def test_long_prompt_blocked(self):
        """Test very long prompt is blocked"""
        long_prompt = "x" * (MAX_PROMPT_LENGTH + 1)
        result = self.orch._validate_prompt(long_prompt)
        self.assertFalse(result)
    
    def test_max_length_prompt(self):
        """Test prompt at max length is accepted"""
        max_prompt = "x" * MAX_PROMPT_LENGTH
        result = self.orch._validate_prompt(max_prompt)
        self.assertTrue(result)


class TestOrchestrator(unittest.TestCase):
    """Test Orchestrator class"""
    
    def setUp(self):
        self.orch = Orchestrator()
    
    def test_init(self):
        """Test orchestrator initialization"""
        self.assertIsNotNone(self.orch.agents_cfg)
        self.assertIsNotNone(self.orch.settings)
    
    def test_get_enabled_agents(self):
        """Test getting enabled agents"""
        enabled = self.orch.get_enabled_agents()
        self.assertIsInstance(enabled, dict)
    
    def test_get_all_agents(self):
        """Test getting all agents"""
        all_agents = self.orch.get_all_agents()
        self.assertIsInstance(all_agents, dict)


if __name__ == "__main__":
    unittest.main()
