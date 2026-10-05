#!/bin/zsh
# Headless ACE Toolkit check: runs the Toolkit's own build and validators (mqsicreatebar -cleanBuild)
# on copies of the given projects, in a scratch Eclipse workspace, so the open Toolkit is not disturbed.
# Prints the Toolkit's problem markers. Exit 0 = no errors (a BAR was built), 1 = errors.
#
# usage: tools/toolkit_check.sh <project-dir> [<project-dir> ...]
# env:   ACE_HOME (default ~/Applications/IBM App Connect Enterprise)
ACE_HOME=${ACE_HOME:-"$HOME/Applications/IBM App Connect Enterprise"}
WS=$(mktemp -d /tmp/toolkit-check.XXXXXX)
apps=()
for p in "$@"; do
  cp -R "$p" "$WS/" || exit 2
  apps+=("$(basename "$p")")
done
cd "$WS"
"$ACE_HOME/tools/mqsicreatebar" -data "$WS" -b "$WS/check.bar" -a "${apps[@]}" -cleanBuild > "$WS/mqsicreatebar.log" 2>&1
rc=$?
if [ $rc -eq 0 ] && [ -f "$WS/check.bar" ]; then
  echo "TOOLKIT CHECK: PASS (0 errors) - projects: ${apps[*]}"
else
  echo "TOOLKIT CHECK: FAIL - projects: ${apps[*]}"
  sed -n '/Problem markers list/,$p' "$WS/mqsicreatebar.log" | grep -E "Problem [0-9]+:" | sed 's/^[[:space:]]*/  /'
  grep -q "Problem markers list" "$WS/mqsicreatebar.log" || tail -15 "$WS/mqsicreatebar.log"
fi
rm -rf "$WS"
[ $rc -eq 0 ]
