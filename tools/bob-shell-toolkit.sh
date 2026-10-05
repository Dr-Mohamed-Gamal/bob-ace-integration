#!/bin/zsh
# Launches IBM Bob Shell from the ACE Toolkit's Local Terminal (Preferences > Terminal > Local Terminal).
# The Toolkit starts terminals with a minimal PATH, so add Homebrew (node, bob) and read the API key file.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
[ -f "$HOME/.bob/bob_api_key" ] && export BOB_API_KEY="$(cat "$HOME/.bob/bob_api_key")"
exec bob "$@"
