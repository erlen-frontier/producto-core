#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 producto-core contributors
# SPDX-License-Identifier: AGPL-3.0-only
"""Licensing compliance checks for producto-core (standard library only).

Checks that LICENSE is the unmodified AGPLv3 text, that required project
files exist, that the README declares AGPL-3.0-only and the section 13
obligations, and that source files carry the expected SPDX headers.
It detects obvious mistakes; it is not legal advice.

Usage: python3 scripts/check_compliance.py [--root PATH]
"""

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

# SHA-256 of the unmodified FSF text of the GNU AGPL v3 (gnu.org/licenses/agpl-3.0.txt).
AGPL_V3_SHA256 = "8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef"
LICENSE_ID = "AGPL-3.0-only"

REQUIRED_FILES = [
    "LICENSE",
    "NOTICE",
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "docs/licensing.md",
    "docs/releasing.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/dco.yml",
    ".github/workflows/release.yml",
]

# README must state these (case-insensitive substrings).
README_MUST_MENTION = [
    f"SPDX-License-Identifier: {LICENSE_ID}",
    "section 13",
    "Corresponding Source",
    "Source",
    "SECURITY.md",
]

CODE_EXTENSIONS = {
    ".py", ".sh", ".bash", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".vue",
    ".svelte", ".css", ".scss", ".html", ".sql", ".go", ".rs", ".java", ".kt",
    ".c", ".h", ".cpp", ".hpp", ".rb", ".php", ".swift",
}
THIRD_PARTY_DIRS = ("third_party/",)
COMPATIBLE_LICENSES = {
    "MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Apache-2.0", "MPL-2.0",
    "LGPL-2.1-or-later", "LGPL-3.0-only", "LGPL-3.0-or-later", "GPL-3.0-only",
    "GPL-3.0-or-later", "AGPL-3.0-only", "AGPL-3.0-or-later", "Zlib",
    "Unlicense", "CC0-1.0", "0BSD",
}
HEADER_LINES = 6  # SPDX lines must appear near the top of the file.
# Captures the SPDX expression, dropping trailing comment closers such as "*/" or "-->".
SPDX_LICENSE = re.compile(r"SPDX-License-Identifier:[ \t]*(.*?)[ \t]*(?:\*/|-->)?[ \t]*$", re.M)
SPDX_COPYRIGHT = re.compile(r"SPDX-FileCopyrightText:\s*\S")


def list_files(root):
    """Tracked files (git ls-files) or, outside a git checkout, a directory walk."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            check=True, capture_output=True,
        ).stdout.decode()
        return sorted({p for p in out.split("\0") if p and (root / p).is_file()})
    except (subprocess.CalledProcessError, FileNotFoundError):
        return sorted(
            p.relative_to(root).as_posix()
            for p in root.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(root).parts
        )


def check_license(root, errors):
    lic = root / "LICENSE"
    if not lic.exists():
        return
    digest = hashlib.sha256(lic.read_bytes()).hexdigest()
    if digest != AGPL_V3_SHA256:
        errors.append("LICENSE: text differs from the unmodified GNU AGPL v3; do not edit the license text")


def check_readme(root, errors):
    readme = root / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8").lower()
    for needle in README_MUST_MENTION:
        if needle.lower() not in text:
            errors.append(f"README.md: must mention '{needle}'")
    if "spdx-license-identifier: agpl-3.0-or-later" in text:
        errors.append("README.md: declares AGPL-3.0-or-later; the project is AGPL-3.0-only")


def check_headers(root, files, errors):
    for rel in files:
        path = root / rel
        if path.suffix not in CODE_EXTENSIONS:
            continue
        try:
            head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:HEADER_LINES])
        except UnicodeDecodeError:
            continue
        ids = SPDX_LICENSE.findall(head)
        third_party = rel.startswith(THIRD_PARTY_DIRS)
        if not ids:
            errors.append(f"{rel}: missing 'SPDX-License-Identifier' in the first {HEADER_LINES} lines")
            continue
        license_id = ids[0].strip()
        if third_party:
            if license_id not in COMPATIBLE_LICENSES:
                errors.append(f"{rel}: third-party license '{license_id}' not in the compatible list; ask for legal review")
        else:
            if license_id != LICENSE_ID:
                errors.append(f"{rel}: SPDX identifier '{license_id}' must be exactly '{LICENSE_ID}'")
            if not SPDX_COPYRIGHT.search(head):
                errors.append(f"{rel}: missing 'SPDX-FileCopyrightText' in the first {HEADER_LINES} lines")


def check(root):
    errors = []
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing {rel}")
    check_license(root, errors)
    check_readme(root, errors)
    check_headers(root, list_files(root), errors)
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)
    errors = check(args.root.resolve())
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(errors)} problem(s)" if errors else "Compliance checks passed.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
