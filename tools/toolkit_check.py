#!/usr/bin/env python3
"""Headless ACE Toolkit check for Bob: python3 ../tools/toolkit_check.py <project> [<project> ...]

Runs the ACE Toolkit's own build and validators (mqsicreatebar -cleanBuild) on copies of the given
ACE projects and prints the Toolkit's problem markers. Exit 0 means no errors. Takes about a minute.
A Python wrapper around toolkit_check.sh so the command matches Bob's pre-approved `python3` prefix.
"""
import os
import subprocess
import sys

script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "toolkit_check.sh")
if len(sys.argv) < 2:
    sys.exit(__doc__)
projects = [os.path.abspath(p) for p in sys.argv[1:]]
sys.exit(subprocess.call(["/bin/zsh", script, *projects]))
