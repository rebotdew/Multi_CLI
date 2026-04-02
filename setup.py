#!/usr/bin/env python3
"""
Multi-Agent AI CLI - Setup Script
Install this package to use 'multi-ai' command globally
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="multi-ai-agent",
    version="1.0.0",
    author="Your Name",
    description="Run multiple AI agents (Codex, Kimi, Qwen, Gemini) in parallel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["cli", "interactive", "controller", "aiswitch", "orchestrator", "skills_registry"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "multi-ai=cli:main",
            "maai=cli:main",
            "multi-ai-i=interactive:main",
            "maai-i=interactive:main",
            "ai-controller=controller:main",
            "aic=controller:main",
            "aiswitch=aiswitch:main",
            "ais=aiswitch:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config.json"],
    },
)
