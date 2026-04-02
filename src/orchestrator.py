"""
orchestrator.py - Core Multi-Agent Execution Engine
รัน AI agents แบบ parallel / sequential / consensus
"""
import asyncio
import json
import os
import sys
import time
import subprocess
import logging
from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Security constants
MAX_PROMPT_LENGTH = 50000  # Max 50K characters
ALLOWED_FILE_EXTENSIONS = {'.txt', '.py', '.js', '.ts', '.md', '.json', '.yaml', '.yml', '.html', '.css', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php'}


# ─── ANSI Colors (Windows compatible) ─────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

AGENT_COLORS = {
    "codex":  C.GREEN,
    "kimi":   C.YELLOW,
    "qwen":   C.MAGENTA,
    "gemini": C.CYAN,
}

LINE = "─" * 60


# ─── Data Classes ──────────────────────────────────────────────────────────────
@dataclass
class AgentResult:
    agent_id: str
    output: str
    error: Optional[str]
    elapsed: float
    success: bool
    cmd_used: list = field(default_factory=list)


@dataclass
class OrchestrationResult:
    prompt: str
    strategy: str
    results: list
    total_elapsed: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ─── Config Loader ─────────────────────────────────────────────────────────────
def load_config(config_path: str = None) -> dict:
    """Load and validate configuration"""
    if config_path is None:
        config_path = Path(__file__).parent / "config.json"
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.warning(f"Config not found: {config_path}, using defaults")
        return _get_default_config()
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config: {e}")
        return _get_default_config()
    
    # Validate config structure
    _validate_config(config)
    return config


def _get_default_config() -> dict:
    """Return default configuration"""
    return {
        "agents": {
            "qwen": {"cmd": "qwen", "cli_args": [], "timeout": 60, "enabled": True},
        },
        "settings": {
            "default_timeout": 60,
            "max_retries": 1,
            "save_outputs": True,
            "show_progress": True,
            "output_dir": "output",
            "log_dir": "logs"
        }
    }


def _validate_config(config: dict) -> None:
    """Validate configuration structure"""
    # Check required keys
    if "agents" not in config:
        logger.warning("Missing 'agents' in config, using defaults")
        config["agents"] = _get_default_config()["agents"]
    
    if "settings" not in config:
        logger.warning("Missing 'settings' in config, using defaults")
        config["settings"] = _get_default_config()["settings"]
    
    # Validate agents
    for agent_id, cfg in config["agents"].items():
        if "cmd" not in cfg:
            logger.warning(f"Agent {agent_id} missing 'cmd', disabling")
            cfg["enabled"] = False
        
        # Validate timeout
        timeout = cfg.get("timeout", 60)
        if not isinstance(timeout, (int, float)) or timeout < 1 or timeout > 600:
            logger.warning(f"Agent {agent_id} timeout {timeout} invalid, setting to 60")
            cfg["timeout"] = 60
    
    # Validate settings
    settings = config["settings"]
    if "output_dir" in settings:
        Path(settings["output_dir"]).mkdir(exist_ok=True)
    if "log_dir" in settings:
        Path(settings["log_dir"]).mkdir(exist_ok=True)


# ─── Orchestrator ──────────────────────────────────────────────────────────────
class Orchestrator:
    def __init__(self, config_path: str = None):
        self.config = load_config(config_path)
        self.agents_cfg = self.config["agents"]
        self.settings = self.config["settings"]
        self._ensure_dirs()
        
        # Setup logging
        log_dir = self.settings.get("log_dir", "logs")
        log_file = Path(log_dir) / f"orchestrator_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    def _ensure_dirs(self):
        for d in [self.settings.get("output_dir", "output"),
                  self.settings.get("log_dir", "logs")]:
            Path(d).mkdir(exist_ok=True)
    
    def _validate_path(self, path: str) -> bool:
        """Security: Prevent path traversal attacks using robust path logic"""
        try:
            p = Path(path).resolve()
            allowed_base = Path.cwd().resolve()
            try:
                p.relative_to(allowed_base)
                return True
            except ValueError:
                # Fallback for case-insensitive Windows comparison
                return str(p).lower().startswith(str(allowed_base).lower())
        except Exception as e:
            logger.warning(f"Path validation failed for {path}: {e}")
            return False
    
    def _validate_file_read(self, path: str) -> bool:
        """Security: Validate file before reading"""
        # Check path traversal
        if not self._validate_path(path):
            logger.warning(f"Path traversal attempt blocked: {path}")
            return False
        
        # Check file extension
        ext = Path(path).suffix.lower()
        if ext and ext not in ALLOWED_FILE_EXTENSIONS:
            logger.warning(f"Blocked file with disallowed extension: {path}")
            return False
        
        # Check if file exists and is a file (not directory)
        if not Path(path).is_file():
            logger.warning(f"File does not exist or is a directory: {path}")
            return False
        
        return True
    
    def _validate_prompt(self, prompt: str) -> bool:
        """Security: Validate prompt length"""
        if len(prompt) > MAX_PROMPT_LENGTH:
            logger.warning(f"Prompt exceeds max length: {len(prompt)} chars")
            return False
        return True

    def get_enabled_agents(self, agent_ids: list = None) -> dict:
        """คืน agents ที่ enabled และอยู่ใน agent_ids (ถ้าระบุ)"""
        result = {}
        for aid, cfg in self.agents_cfg.items():
            if not cfg.get("enabled", False):
                continue
            if agent_ids and aid not in agent_ids:
                continue
            result[aid] = cfg
        return result

    def get_all_agents(self) -> dict:
        return self.agents_cfg

    def build_cmd(self, agent_id: str, prompt: str) -> list:
        cfg = self.agents_cfg[agent_id]
        # Basic sanitization for shell metacharacters
        sanitized = prompt.replace('$', '').replace('`', '').replace('\\', '')
        cmd = [cfg["cmd"]] + cfg.get("cli_args", cfg.get("args", []))
        cmd.append(sanitized)
        return cmd

    # ─── Async single agent ──────────────────────────────────────────────────
    async def _run_agent_async(self, agent_id: str, prompt: str,
                                timeout: int = None) -> AgentResult:
        cfg = self.agents_cfg[agent_id]
        to = timeout or cfg.get("timeout", self.settings["default_timeout"])
        cmd = self.build_cmd(agent_id, prompt)
        start = time.time()

        env = os.environ.copy()
        env.update(cfg.get("env_vars", {}))

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=to)
            except asyncio.TimeoutError:
                proc.kill()
                await proc.communicate()
                return AgentResult(agent_id=agent_id, output="",
                    error=f"Timeout หลังจาก {to}s", elapsed=time.time()-start,
                    success=False, cmd_used=cmd)

            elapsed = time.time() - start
            if proc.returncode == 0:
                out = stdout.decode("utf-8", errors="replace").strip()
                max_chars = self.settings.get("max_output_chars", 3000)
                if len(out) > max_chars:
                    out = out[:max_chars] + f"\n{C.DIM}... (ตัดที่ {max_chars} ตัวอักษร){C.RESET}"
                return AgentResult(agent_id=agent_id, output=out,
                    error=None, elapsed=elapsed, success=True, cmd_used=cmd)
            else:
                err = stderr.decode("utf-8", errors="replace").strip()
                return AgentResult(agent_id=agent_id, output="",
                    error=err or f"Exit {proc.returncode}",
                    elapsed=time.time()-start, success=False, cmd_used=cmd)

        except FileNotFoundError:
            return AgentResult(agent_id=agent_id, output="",
                error=f"ไม่พบคำสั่ง '{cmd[0]}' — ตรวจสอบว่าติดตั้งและอยู่ใน PATH",
                elapsed=time.time()-start, success=False, cmd_used=cmd)
        except Exception as e:
            return AgentResult(agent_id=agent_id, output="",
                error=str(e), elapsed=time.time()-start, success=False, cmd_used=cmd)

    # ─── Execution Strategies ────────────────────────────────────────────────
    async def run_parallel(self, agent_ids: list, prompt: str) -> list:
        """รันทุก agent พร้อมกัน"""
        tasks = [self._run_agent_async(aid, prompt) for aid in agent_ids]
        return list(await asyncio.gather(*tasks))

    async def run_sequential(self, agent_ids: list, prompt: str) -> list:
        """รัน agent ทีละตัวตามลำดับ"""
        results = []
        for aid in agent_ids:
            r = await self._run_agent_async(aid, prompt)
            results.append(r)
        return results

    async def run_single(self, agent_id: str, prompt: str) -> AgentResult:
        return await self._run_agent_async(agent_id, prompt)

    # ─── Sync wrappers ───────────────────────────────────────────────────────
    def _get_event_loop(self):
        """Get or create event loop safely and set it as current"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, create a new one for sync context
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                return new_loop
            return loop
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
    
    def parallel(self, agent_ids: list, prompt: str) -> list:
        """Run agents in parallel (sync wrapper)"""
        # Validate prompt
        if not self._validate_prompt(prompt):
            return [AgentResult("validation", "", f"Prompt ยาวเกิน {MAX_PROMPT_LENGTH} ตัวอักษร", 0, False)]
        
        loop = self._get_event_loop()
        try:
            return loop.run_until_complete(self.run_parallel(agent_ids, prompt))
        finally:
            # Note: We don't close the loop here to avoid issues with subsequent calls
            pass

    def sequential(self, agent_ids: list, prompt: str) -> list:
        """Run agents sequentially (sync wrapper)"""
        # Validate prompt
        if not self._validate_prompt(prompt):
            return [AgentResult("validation", "", f"Prompt ยาวเกิน {MAX_PROMPT_LENGTH} ตัวอักษร", 0, False)]
        
        loop = self._get_event_loop()
        try:
            return loop.run_until_complete(self.run_sequential(agent_ids, prompt))
        finally:
            pass

    def single(self, agent_id: str, prompt: str) -> AgentResult:
        """Run single agent (sync wrapper)"""
        # Validate prompt
        if not self._validate_prompt(prompt):
            return AgentResult("validation", "", f"Prompt ยาวเกิน {MAX_PROMPT_LENGTH} ตัวอักษร", 0, False)
        
        loop = self._get_event_loop()
        try:
            return loop.run_until_complete(self.run_single(agent_id, prompt))
        finally:
            pass

    # ─── Save output ─────────────────────────────────────────────────────────
    def save_result(self, prompt: str, results: list, strategy: str = ""):
        if not self.settings.get("save_outputs", True):
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = Path(self.settings["output_dir"]) / f"result_{ts}.json"
        data = {
            "timestamp": ts,
            "prompt": prompt,
            "strategy": strategy,
            "results": [
                {
                    "agent": r.agent_id,
                    "success": r.success,
                    "elapsed": round(r.elapsed, 2),
                    "output": r.output,
                    "error": r.error,
                }
                for r in results
            ],
        }
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# ─── Display Helpers ───────────────────────────────────────────────────────────
def color_for(agent_id: str) -> str:
    return AGENT_COLORS.get(agent_id, C.WHITE)

def print_result(result: AgentResult, show_cmd: bool = False):
    col = color_for(result.agent_id)
    name = result.agent_id.upper()
    elapsed = f"{result.elapsed:.1f}s"

    if result.success:
        print(f"\n{col}{C.BOLD}✓ {name} ({elapsed}){C.RESET}")
        print(LINE)
        print(result.output)
    else:
        print(f"\n{C.RED}{C.BOLD}✗ {name} ({elapsed}){C.RESET}")
        print(LINE)
        print(f"{C.RED}Error: {result.error}{C.RESET}")

    if show_cmd:
        print(f"{C.DIM}CMD: {' '.join(result.cmd_used)}{C.RESET}")

def print_results(results: list, show_cmd: bool = False):
    for r in results:
        print_result(r, show_cmd)
    print()

def print_summary(results: list):
    """สรุปผลทุก agent"""
    print(f"\n{C.BOLD}{'─'*60}")
    print(f"{'Agent':<10} {'สถานะ':<10} {'เวลา':<10} {'ความยาว'}")
    print(f"{'─'*60}{C.RESET}")
    for r in results:
        col = color_for(r.agent_id)
        status = f"{C.GREEN}✓ สำเร็จ{C.RESET}" if r.success else f"{C.RED}✗ ผิดพลาด{C.RESET}"
        length = f"{len(r.output)} chars" if r.success else "-"
        print(f"{col}{r.agent_id.upper():<10}{C.RESET} {status:<20} {r.elapsed:.1f}s{'':<8} {length}")
    print()
