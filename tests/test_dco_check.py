# SPDX-FileCopyrightText: 2026 producto-core contributors
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for scripts/dco-check.sh."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from helpers import GIT_ENV, SCRIPTS, commit, git, init_repo

SCRIPT = SCRIPTS / "dco-check.sh"
SIGNOFF = "\n\nSigned-off-by: Test Author <author@example.com>"
OTHER = {"GIT_AUTHOR_NAME": "Other", "GIT_AUTHOR_EMAIL": "other@example.com"}


def dco(repo, base, head):
    return subprocess.run(
        ["bash", str(SCRIPT), base, head], cwd=repo, capture_output=True, text=True, env=GIT_ENV
    )


class DcoCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = init_repo(self.tmp / "repo")
        self.base = commit(self.repo, "a.txt", "a\n", "chore: base")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_signed_commits_pass(self):
        commit(self.repo, "b.txt", "b\n", "feat: b" + SIGNOFF)
        head = commit(self.repo, "c.txt", "c\n", "fix: c" + SIGNOFF.replace("author@", "AUTHOR@"))
        result = dco(self.repo, self.base, head)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("All 2 commit(s) are signed off.", result.stdout)

    def test_unsigned_commit_fails(self):
        commit(self.repo, "b.txt", "b\n", "feat: b" + SIGNOFF)
        head = commit(self.repo, "c.txt", "c\n", "fix: c")
        result = dco(self.repo, self.base, head)
        self.assertEqual(result.returncode, 1)
        self.assertIn("has no Signed-off-by line", result.stdout)

    def test_signoff_of_someone_else_fails(self):
        head = commit(self.repo, "b.txt", "b\n", "feat: b" + SIGNOFF, env=OTHER)
        result = dco(self.repo, self.base, head)
        self.assertEqual(result.returncode, 1)
        self.assertIn("no Signed-off-by matching its author", result.stdout)

    def test_signoff_in_body_text_is_not_a_trailer(self):
        head = commit(self.repo, "b.txt", "b\n", "feat: b\n\nSigned-off-by: Test Author <author@example.com> was here\n\nMore text")
        result = dco(self.repo, self.base, head)
        self.assertEqual(result.returncode, 1)

    def test_merge_commits_are_skipped(self):
        git(self.repo, "checkout", "-q", "-b", "topic")
        commit(self.repo, "b.txt", "b\n", "feat: b" + SIGNOFF)
        git(self.repo, "checkout", "-q", "main")
        commit(self.repo, "c.txt", "c\n", "chore: main moves" + SIGNOFF)
        git(self.repo, "checkout", "-q", "topic")
        git(self.repo, "merge", "-q", "--no-ff", "-m", "Merge main into topic", "main")
        head = git(self.repo, "rev-parse", "HEAD")
        result = dco(self.repo, self.base, head)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_empty_range_passes(self):
        result = dco(self.repo, self.base, self.base)
        self.assertEqual(result.returncode, 0)
        self.assertIn("No commits to check.", result.stdout)


if __name__ == "__main__":
    unittest.main()
