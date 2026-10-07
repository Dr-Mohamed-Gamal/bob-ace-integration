#!/bin/zsh
# Launches IBM Bob Shell from the ACE Toolkit's Local Terminal (Preferences > Terminal > Local Terminal).
# The Toolkit starts terminals with a minimal PATH, so add Homebrew (node, bob) and read the API key file.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
[ -f "$HOME/.bob/bob_api_key" ] && export BOB_API_KEY="$(cat "$HOME/.bob/bob_api_key")"
# The Toolkit's terminal does not report its size to the programs it runs. Set COLUMNS and LINES so Bob Shell
# has a fixed size to lay out its screen; without them, Bob Shell could not start commands after a long step.
[ "${COLUMNS:-0}" -gt 0 ] 2>/dev/null || COLUMNS=120
[ "${LINES:-0}" -gt 0 ] 2>/dev/null || LINES=40
export COLUMNS LINES
exec bob "$@"
