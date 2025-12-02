#!/usr/bin/env python3
"""
Todo List Command Line Tool
A simple CLI tool for managing tasks and time-aware habits
"""

# Add src directory to path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.cli import TodoCLI

if __name__ == '__main__':
    TodoCLI().cmdloop()
