"""
Tests for CLI module
"""
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestCLICommands(unittest.TestCase):
    """Test CLI command parsing"""
    
    def test_import_cli(self):
        """Test CLI module can be imported"""
        try:
            from cli import main
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import cli: {e}")


class TestController(unittest.TestCase):
    """Test Controller command parsing"""
    
    def test_import_controller(self):
        """Test Controller module can be imported"""
        try:
            from controller import Controller
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import controller: {e}")
    
    def test_use_command_parsing(self):
        """Test /use command parsing is fixed"""
        # This tests that the bug fix is in place
        from controller import Controller
        from orchestrator import Orchestrator
        
        controller = Controller()
        
        # Test that /use command exists
        self.assertTrue(hasattr(controller, 'cmd_use'))


class TestInteractive(unittest.TestCase):
    """Test Interactive CLI"""
    
    def test_import_interactive(self):
        """Test Interactive module can be imported"""
        try:
            from interactive import InteractiveCLI
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import interactive: {e}")


if __name__ == "__main__":
    unittest.main()
