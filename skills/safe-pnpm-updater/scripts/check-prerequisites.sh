#!/usr/bin/env bash
set -euo pipefail

project_dir="${1:-$PWD}"

fail() {
  printf 'SAFE_DEPENDENCY_UPDATE_BLOCKED: %s\n' "$*" >&2
  exit 1
}

if [[ ! -d "$project_dir" ]]; then
  fail "project directory does not exist: $project_dir"
fi
project_dir="$(cd "$project_dir" && pwd -P)"

if [[ ! -f "$project_dir/package.json" ]]; then
  fail "project root does not contain package.json: $project_dir"
fi

if ! command -v zsh >/dev/null 2>&1; then
  fail "zsh is unavailable; cannot verify the configured Socket Firewall alias"
fi

zsh_in_project() {
  (cd "$project_dir" && zsh -ic "$1")
}

alias_output="$(zsh_in_project 'alias pnpm' 2>&1)" ||
  fail "could not inspect the interactive pnpm alias"

if ! grep -Eq "pnpm=['\"]sfw --verbose pnpm['\"]" <<<"$alias_output"; then
  fail "pnpm is not the exact 'sfw --verbose pnpm' alias"
fi

sfw_path="$(zsh_in_project 'whence -p sfw' 2>/dev/null | awk 'NF { value = $0 } END { print value }')"
if [[ -z "$sfw_path" || ! -x "$sfw_path" ]]; then
  fail "sfw does not resolve to an executable"
fi

version_output="$(zsh_in_project 'pnpm --version' 2>&1)" ||
  fail "the Socket Firewall-routed pnpm command could not run"
if ! grep -Fq 'Protected by Socket Firewall' <<<"$version_output"; then
  fail "the aliased pnpm command did not provide Socket Firewall runtime confirmation"
fi

pnpm_version="$(printf '%s\n' "$version_output" | awk '/^[0-9]+(\.[0-9]+){2}([+-][0-9A-Za-z.-]+)?$/ { value = $0 } END { print value }')"
if [[ -z "$pnpm_version" ]]; then
  fail "could not read the pnpm version through Socket Firewall"
fi

age_output="$(zsh_in_project 'pnpm config get minimumReleaseAge' 2>&1)" ||
  fail "could not read pnpm minimumReleaseAge through Socket Firewall"
if ! grep -Fq 'Protected by Socket Firewall' <<<"$age_output"; then
  fail "the minimumReleaseAge check was not routed through Socket Firewall"
fi

minimum_release_age="$(printf '%s\n' "$age_output" | awk '$0 ~ /^[0-9]+([.][0-9]+)?$/ { value = $0 } END { print value }')"
if [[ -z "$minimum_release_age" ]] ||
  ! awk -v age="$minimum_release_age" 'BEGIN { exit !(age > 0) }'; then
  fail "pnpm minimumReleaseAge must be a positive number of minutes"
fi

printf 'SAFE_DEPENDENCY_UPDATE_PREREQUISITES_OK\n'
printf 'socket_firewall: sfw (%s), alias and runtime confirmation verified\n' "$sfw_path"
printf 'pnpm: %s\n' "$pnpm_version"
printf 'minimumReleaseAge_minutes: %s\n' "$minimum_release_age"
