#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 producto-core contributors
# SPDX-License-Identifier: AGPL-3.0-only
#
# Developer Certificate of Origin check (pure bash + git).
# Usage: scripts/dco-check.sh <base> <head>
# Every non-merge commit in <base>..<head> needs a "Signed-off-by:" trailer
# whose e-mail matches the commit author's e-mail (case-insensitive).
set -euo pipefail

base=${1:?usage: dco-check.sh <base> <head>}
head=${2:?usage: dco-check.sh <base> <head>}

commits=$(git rev-list --no-merges --reverse "${base}..${head}")
if [ -z "$commits" ]; then
  echo "No commits to check."
  exit 0
fi

failed=0
total=0
for c in $commits; do
  total=$((total + 1))
  author_email=$(git show -s --format='%ae' "$c" | tr '[:upper:]' '[:lower:]')
  subject=$(git show -s --format='%s' "$c")
  signoffs=$(git show -s --format='%(trailers:key=Signed-off-by,valueonly,unfold)' "$c" | tr '[:upper:]' '[:lower:]')
  if [ -z "$signoffs" ]; then
    echo "::error::${c:0:12} \"${subject}\" has no Signed-off-by line."
    failed=$((failed + 1))
  elif ! grep -qF "<${author_email}>" <<<"$signoffs"; then
    echo "::error::${c:0:12} \"${subject}\" has no Signed-off-by matching its author e-mail."
    failed=$((failed + 1))
  else
    echo "ok ${c:0:12} ${subject}"
  fi
done

if [ "$failed" -gt 0 ]; then
  echo
  echo "${failed} of ${total} commit(s) lack a valid DCO sign-off. See CONTRIBUTING.md."
  echo "Fix: git rebase --signoff <base branch> && git push --force-with-lease"
  echo "Only a human can sign off: AI agents must not add Signed-off-by lines."
  exit 1
fi
echo "All ${total} commit(s) are signed off."
