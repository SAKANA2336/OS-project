#!/usr/bin/env bash

set -euo pipefail

usage() {
  printf 'Usage: %s <work|release>\n' "$0" >&2
  exit 2
}

fail() {
  printf 'workspace-zone check failed: %s\n' "$1" >&2
  exit 1
}

check_origin_url() {
  local label="$1"
  local value="$2"
  [[ "$value" == 'https://github.com/SAKANA2336/OS-project.git' ]] ||
    fail "unexpected origin $label URL: $value"
}

resolve_git_path() {
  local value="$1"
  if [[ "$value" == /* ]]; then
    (cd "$value" && pwd -P)
  else
    (cd "$root/$value" && pwd -P)
  fi
}

[[ $# -eq 1 ]] || usage
role="$1"

root="$(git rev-parse --show-toplevel 2>/dev/null)" || fail 'not inside a Git repository'
root="$(cd "$root" && pwd -P)"
root_name="$(basename "$root")"
bootstrap_commit='62b2d649e2c4ffdb91eeb7bf4c2932be5a9023ba'

[[ -d "$root/.git" ]] ||
  fail 'the zone must be an independent repository with a .git directory; linked worktrees are not allowed'

git_dir="$(resolve_git_path "$(git rev-parse --git-dir)")"
common_dir="$(resolve_git_path "$(git rev-parse --git-common-dir)")"
expected_git_dir="$(cd "$root/.git" && pwd -P)"
[[ "$git_dir" == "$expected_git_dir" && "$common_dir" == "$expected_git_dir" ]] ||
  fail 'Git metadata is shared or located outside this independent repository'
git merge-base --is-ancestor "$bootstrap_commit" HEAD 2>/dev/null ||
  fail 'repository history does not descend from the verified OS-project bootstrap commit'

marker="$root/.local/workspace-role"
[[ -f "$marker" ]] || fail 'missing local role marker .local/workspace-role'
marker_role="$(tr -d '[:space:]' < "$marker")"
[[ "$marker_role" == "$role" ]] ||
  fail "role marker says '$marker_role', requested '$role'"

remote_list="$(git remote)"

case "$role" in
  work)
    [[ "$root_name" == 'OS-project-local' ]] ||
      fail "daily work zone directory must be named OS-project-local, got: $root_name"
    if [[ -n "$remote_list" ]]; then
      printf 'detected remotes:\n' >&2
      git remote -v >&2
      fail 'the daily work zone must not configure any remote'
    fi
    ;;
  release)
    case "$root_name" in
      OS-project)
        ;;
      'os project')
        printf 'warning: accepting legacy bootstrap release directory name: %s\n' "$root_name" >&2
        ;;
      *)
        fail "release zone directory must be named OS-project, got: $root_name"
        ;;
    esac
    if [[ "$remote_list" != "origin" ]]; then
      printf 'detected remotes:\n' >&2
      git remote -v >&2 || true
      fail 'the release zone must configure only origin'
    fi
    fetch_url="$(git remote get-url --all origin)"
    push_url="$(git remote get-url --push --all origin)"
    check_origin_url 'fetch' "$fetch_url"
    check_origin_url 'push' "$push_url"
    [[ "$(git branch --show-current)" == 'main' ]] ||
      fail 'release zone must be on main'
    upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
    [[ "$upstream" == 'origin/main' ]] ||
      fail "release main must track origin/main, got: ${upstream:-none}"
    ;;
  *)
    usage
    ;;
esac

printf 'workspace-zone check passed\n'
printf 'role: %s\n' "$role"
printf 'root: %s\n' "$root"
