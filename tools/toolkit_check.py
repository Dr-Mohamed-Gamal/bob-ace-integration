#!/usr/bin/env python3
"""Headless ACE Toolkit check: python3 ../tools/toolkit_check.py <project> [<project> ...]

Runs the ACE Toolkit's own build and validators (mqsicreatebar -cleanBuild) on copies of the given
ACE projects, in a scratch Eclipse workspace, so the open Toolkit is not disturbed. Prints the
Toolkit's problem markers. Exit 0 = no errors (a BAR was built), 1 = errors, 2 = ACE not found.
It reports errors only; warnings show in the Toolkit's Problems view.

Works on Windows, macOS and Linux. ACE is found from the ACE_HOME environment variable (the ACE
installation folder, the one that contains `tools/`), else from the usual install locations.
"""
import glob
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile


def count_compiled_flows(bar):
    """Count compiled flows (.cmf) in the BAR, including inside nested application archives."""
    count = 0
    with zipfile.ZipFile(bar) as z:
        for name in z.namelist():
            if name.endswith(".cmf"):
                count += 1
            elif name.endswith((".appzip", ".libzip", ".shlibzip", ".zip")):
                inner = os.path.join(os.path.dirname(bar), "inner-" + os.path.basename(name))
                with open(inner, "wb") as f:
                    f.write(z.read(name))
                count += count_compiled_flows(inner)
    return count


def find_mqsicreatebar():
    names = ["mqsicreatebar.exe", "mqsicreatebar.bat"] if platform.system() == "Windows" else ["mqsicreatebar"]
    homes = []
    if os.environ.get("ACE_HOME"):
        homes.append(os.environ["ACE_HOME"])
    if platform.system() == "Windows":
        for root in (os.environ.get("ProgramFiles", r"C:\Program Files"), r"C:\IBM"):
            homes += sorted(glob.glob(os.path.join(root, "IBM", "ACE", "*")), reverse=True)
            homes += sorted(glob.glob(os.path.join(root, "ACE", "*")), reverse=True)
    elif platform.system() == "Darwin":
        homes += [os.path.expanduser("~/Applications/IBM App Connect Enterprise"),
                  "/Applications/IBM App Connect Enterprise"]
    else:
        homes += sorted(glob.glob("/opt/IBM/ace-*"), reverse=True) + sorted(glob.glob("/opt/ibm/ace-*"), reverse=True)
    for home in homes:
        for name in names:
            path = os.path.join(home, "tools", name)
            if os.path.isfile(path):
                return path
    return shutil.which("mqsicreatebar")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    exe = find_mqsicreatebar()
    if not exe:
        print("TOOLKIT CHECK: NOT RUN - mqsicreatebar not found. Set ACE_HOME to the ACE installation folder,"
              " or refresh the project in the Toolkit and read the Problems view.")
        sys.exit(2)
    workspace = tempfile.mkdtemp(prefix="toolkit-check-")
    try:
        apps = []
        for project in sys.argv[1:]:
            project = os.path.abspath(project)
            name = os.path.basename(project.rstrip("/\\"))
            shutil.copytree(project, os.path.join(workspace, name))
            apps.append(name)
        bar = os.path.join(workspace, "check.bar")
        cmd = [exe, "-data", workspace, "-b", bar, "-a", *apps, "-cleanBuild"]
        run = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True, errors="replace")
        log = run.stdout + run.stderr
        if run.returncode == 0 and os.path.isfile(bar):
            flows = count_compiled_flows(bar)
            if flows == 0:
                print(f"TOOLKIT CHECK: FAIL - projects: {' '.join(apps)}")
                print("  The BAR contains no compiled flows: the Toolkit did not recognise the project as an ACE"
                      " project. Compare .project, the descriptor and the flow files with the ace-flowpilot examples.")
                return 1
            print(f"TOOLKIT CHECK: PASS (0 errors, {flows} compiled flows) - projects: {' '.join(apps)}")
            return 0
        print(f"TOOLKIT CHECK: FAIL - projects: {' '.join(apps)}")
        problems = re.findall(r"Problem \d+:.*", log)
        for line in problems:
            print("  " + line.strip())
        if not problems:
            print("\n".join("  " + l for l in log.strip().splitlines()[-15:]))
        return 1
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
