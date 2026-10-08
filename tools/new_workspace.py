#!/usr/bin/env python3
"""Create the Bob workspace for this kit next to the tools folder: python3 tools/new_workspace.py [folder]

Default folder: bob-workspace in the repository root (the rules and prompts refer to the tools as
../tools/, so the workspace sits one level below them). What it creates:

  bob-workspace/
    .bob/rules/client-standards.md     copied from RULES/
    .bob/rules/ibm-working-method.md   copied from RULES/
    .bobignore                         hides the Toolkit's second skill copy and its metadata from Bob
    requirements/                      put the two requirement documents here (not in this repository)
    templates/                         put the Interface Definition Document template here (.md and .docx)
    tests/  docs/                      Bob writes the cases file and the documents here

Then open the ACE Toolkit on this folder: it installs IBM's ace-flowpilot skill into .bob/skills/ itself.
Run again to refresh the rules from RULES/ (other files are left alone).
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = {
    "requirements": ["API-SRS-Project_MOCK_Loyalty_Rewards-V1.0.md",
                     "API_SRS-MOCK_Loyalty_Partner_Redemption_Changes_V1.0.md"],
    "templates": ["EAI_Interface_Definition_Document_TEMPLATE.md", "EAI_Interface_Definition_Document_TEMPLATE.docx"],
}


def main():
    ws = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "bob-workspace")
    rules = os.path.join(ws, ".bob", "rules")
    os.makedirs(rules, exist_ok=True)
    for name in ("client-standards.md", "ibm-working-method.md"):
        shutil.copy(os.path.join(ROOT, "RULES", name), os.path.join(rules, name))
    ignore = os.path.join(ws, ".bobignore")
    ignore_new = not os.path.exists(ignore)
    if ignore_new:
        open(ignore, "w").write("# The Toolkit's second copy of the ace-flowpilot skill (Bob uses .bob/skills) and Eclipse metadata\n"
                                ".github/\n.metadata/\n")
    for folder in ("requirements", "templates", "tests", "docs"):
        os.makedirs(os.path.join(ws, folder), exist_ok=True)
    print(f"Workspace: {ws}")
    print("  .bob/rules/        two rules files copied from RULES/")
    print("  .bobignore         " + ("written" if ignore_new else "kept"))
    missing = []
    for folder, names in REQUIRED.items():
        for n in names:
            if not os.path.exists(os.path.join(ws, folder, n)):
                missing.append(f"{folder}/{n}")
    if missing:
        print("Still needed (ask the pilot lead; these documents are not in the repository):")
        for m in missing:
            print("  " + m)
    else:
        print("  requirements/ and templates/ complete")
    print("Next: open the ACE Toolkit on this folder, add the 'IBM Bob Shell' terminal entry (tools/bob-shell-toolkit.sh),")
    print("      Window > Show View > Terminal, and send prompt 1 from use-case-1-create-service/prompts/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
