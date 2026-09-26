# SPDX-FileCopyrightText: 2026 producto-core contributors
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for scripts/check_compliance.py."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import ROOT, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import check_compliance  # noqa: E402

HEADER = "# SPDX-FileCopyrightText: 2026 producto-core contributors\n# SPDX-License-Identifier: AGPL-3.0-only\n"


class ComplianceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "repo"  # not a git checkout: the checker walks the tree
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", "dist"))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def assertProblem(self, fragment):
        errors = check_compliance.check(self.root)
        self.assertTrue(any(fragment in e for e in errors), f"{fragment!r} not in {errors}")

    def test_repository_passes(self):
        self.assertEqual(check_compliance.check(ROOT), [])

    def test_copy_passes(self):
        self.assertEqual(check_compliance.check(self.root), [])

    def test_modified_license_fails(self):
        with open(self.root / "LICENSE", "a", encoding="utf-8") as f:
            f.write("\nExtra terms.\n")
        self.assertProblem("LICENSE: text differs")

    def test_missing_required_file_fails(self):
        (self.root / "SECURITY.md").unlink()
        self.assertProblem("missing SECURITY.md")

    def test_readme_without_section_13_fails(self):
        text = (self.root / "README.md").read_text(encoding="utf-8").replace("section 13", "s13")
        self.write("README.md", text)
        self.assertProblem("must mention 'section 13'")

    def test_source_file_without_header_fails(self):
        self.write("src/app.py", "print('hi')\n")
        self.assertProblem("src/app.py: missing 'SPDX-License-Identifier'")

    def test_or_later_identifier_fails(self):
        self.write("src/app.js", "// SPDX-FileCopyrightText: 2026 x\n// SPDX-License-Identifier: AGPL-3.0-or-later\n")
        self.assertProblem("must be exactly 'AGPL-3.0-only'")

    def test_missing_copyright_text_fails(self):
        self.write("src/app.ts", "// SPDX-License-Identifier: AGPL-3.0-only\n")
        self.assertProblem("missing 'SPDX-FileCopyrightText'")

    def test_valid_headers_pass(self):
        self.write("src/app.py", "#!/usr/bin/env python3\n" + HEADER + "print('hi')\n")
        self.write("src/style.css", "/* SPDX-FileCopyrightText: 2026 x */\n/* SPDX-License-Identifier: AGPL-3.0-only */\n")
        self.write("src/page.html", "<!-- SPDX-FileCopyrightText: 2026 x -->\n<!-- SPDX-License-Identifier: AGPL-3.0-only -->\n")
        self.assertEqual(check_compliance.check(self.root), [])

    def test_third_party_compatible_license_passes(self):
        self.write("third_party/lib/lib.js", "// SPDX-License-Identifier: MIT\n")
        self.assertEqual(check_compliance.check(self.root), [])

    def test_third_party_incompatible_license_fails(self):
        self.write("third_party/lib/lib.js", "// SPDX-License-Identifier: GPL-2.0-only\n")
        self.assertProblem("not in the compatible list")

    def test_docs_and_data_do_not_need_headers(self):
        self.write("docs/extra.md", "# Notes\n")
        self.write("data/example.json", "{}\n")
        self.assertEqual(check_compliance.check(self.root), [])


if __name__ == "__main__":
    unittest.main()
