#!/usr/bin/env python3
"""Hand a project folder to the running ACE Toolkit, which opens its import wizard for it.
usage: python3 tools/toolkit_import.py <project folder>

The Toolkit (Eclipse 4.31) opens the "Import Projects from File System or Archive" wizard when a
folder is passed to the running instance. The developer checks the project it lists and clicks Finish:
no menu navigation, no browsing. If no Toolkit is running, the command starts one.

  macOS    open -g -a "<ACE>/tools/Eclipse.app" <folder>          (tested, ACE 13.0.9)
  Windows  "<ACE>\\tools\\eclipse.exe" --launcher.openFile <folder>   (the launcher relays to the running
                                                                    instance; not yet tried on Windows)
  Linux    "<ACE>/tools/eclipse" --launcher.openFile <folder>       (not yet tried)

ACE is found like runtime_check.py does: ACE_HOME, or the usual install folders. Exit 0 = handed over,
2 = ACE or the Toolkit not found.
"""
import glob
import os
import platform
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from runtime_check import ace_home
except ImportError:  # runtime_check.py not next to this file
    def ace_home():
        return os.environ.get("ACE_HOME")


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit(__doc__)
    folder = os.path.abspath(sys.argv[1])
    if not os.path.isfile(os.path.join(folder, ".project")):
        print(f"TOOLKIT IMPORT: {folder} has no .project file; the Toolkit will not recognise it as a project")
    home = ace_home()
    if not home:
        print("TOOLKIT IMPORT: NOT RUN - ACE not found. Set ACE_HOME to the ACE installation folder.")
        return 2
    system = platform.system()
    if system == "Darwin":
        app = os.path.join(home, "tools", "Eclipse.app")
        cmd = ["open", "-g", "-a", app, folder]
    elif system == "Windows":
        exe = next(iter(glob.glob(os.path.join(home, "tools", "eclipse.exe"))), None)
        if not exe:
            print(f"TOOLKIT IMPORT: NOT RUN - no tools\\eclipse.exe under {home}")
            return 2
        cmd = [exe, "--launcher.openFile", folder]
    else:
        exe = os.path.join(home, "tools", "eclipse")
        cmd = [exe, "--launcher.openFile", folder]
    rc = subprocess.run(cmd).returncode
    if rc != 0:
        print(f"TOOLKIT IMPORT: FAIL - {' '.join(cmd)} returned {rc}")
        return 2
    print(f"TOOLKIT IMPORT: handed {os.path.basename(folder)} to the Toolkit. In the Toolkit, the import wizard "
          f"opens with this folder: check the project is listed and click Finish.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
