#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 producto-core contributors
# SPDX-License-Identifier: AGPL-3.0-only
#
# Build a reproducible source archive of a git ref, plus SOURCE.json.
# Usage: scripts/source-archive.sh <ref> [<output dir>] [<label>]
#   <ref>    commit, tag or branch to archive (e.g. v1.2.3, HEAD)
#   <label>  name used in the file name (default: the ref, or the short
#            commit when the ref is not a tag)
# The same commit produces byte-identical output with the same git and gzip
# versions: git archive stores the commit time as file time and gzip -n
# omits the name and time stamp. No network access and no secrets needed.
set -euo pipefail

ref=${1:?usage: source-archive.sh <ref> [<output dir>] [<label>]}
out=${2:-dist}
repo_url=${SOURCE_REPOSITORY_URL:-https://github.com/erlen-frontier/producto-core}

commit=$(git rev-parse --verify --quiet "${ref}^{commit}") || { echo "error: unknown ref '$ref'" >&2; exit 1; }
if [ -n "${3:-}" ]; then
  label=$3
elif git rev-parse --verify --quiet "refs/tags/${ref}" >/dev/null; then
  label=$ref
else
  label=$(git rev-parse --short=12 "$commit")
fi
case $label in
  *[!A-Za-z0-9._-]*|'') echo "error: invalid label '$label'" >&2; exit 1 ;;
esac

name="producto-core-${label}"
mkdir -p "$out"
archive="$out/${name}.tar.gz"
git -c core.autocrlf=false archive --format=tar --prefix="${name}/" "$commit" | gzip -n -9 > "$archive"
sha=$(sha256sum "$archive" | cut -d' ' -f1)

cat > "$out/SOURCE.json" <<JSON
{
  "name": "producto-core",
  "license": "AGPL-3.0-only",
  "repository": "${repo_url}",
  "ref": "${label}",
  "commit": "${commit}",
  "source_url": "${repo_url}/tree/${commit}",
  "archive": "${name}.tar.gz",
  "archive_sha256": "${sha}"
}
JSON
echo "${sha}  ${archive}"
