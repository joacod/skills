#!/usr/bin/env bash
set -euo pipefail

if (( $# == 0 )); then
  printf 'Usage: %s <pnpm-arguments...>\n' "$0" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "$0")" && pwd -P)"
project_dir="${DEPENDENCY_UPDATE_PROJECT_DIR:-$PWD}"

"$script_dir/check-prerequisites.sh" "$project_dir" >&2
cd "$project_dir"

# The command string is parsed after .zshrc is loaded, so pnpm expands to the
# user's verified Socket Firewall alias. Positional arguments stay quoted.
exec zsh -ic 'pnpm "$@"' safe-pnpm-updater "$@"
