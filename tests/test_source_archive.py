# SPDX-FileCopyrightText: 2026 producto-core contributors
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for scripts/source-archive.sh."""

import hashlib
import json
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

from helpers import GIT_ENV, SCRIPTS, commit, git, init_repo

SCRIPT = SCRIPTS / "source-archive.sh"


def run(repo, *args):
    return subprocess.run(
        ["bash", str(SCRIPT), *args], cwd=repo, check=True, capture_output=True, text=True, env=GIT_ENV
    )


class SourceArchiveTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo = init_repo(self.tmp / "repo")
        commit(self.repo, "LICENSE", "license text\n", "chore: add license")
        self.sha = commit(self.repo, "main.py", "print('hi')\n", "feat: add main")
        git(self.repo, "tag", "v1.0.0")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_same_commit_is_byte_identical(self):
        run(self.repo, "v1.0.0", str(self.tmp / "a"))
        run(self.repo, "v1.0.0", str(self.tmp / "b"))
        a = (self.tmp / "a/producto-core-v1.0.0.tar.gz").read_bytes()
        b = (self.tmp / "b/producto-core-v1.0.0.tar.gz").read_bytes()
        self.assertEqual(a, b)

    def test_source_json_links_commit_and_archive(self):
        run(self.repo, "v1.0.0", str(self.tmp / "out"))
        meta = json.loads((self.tmp / "out/SOURCE.json").read_text())
        archive = self.tmp / "out" / meta["archive"]
        self.assertEqual(meta["commit"], self.sha)
        self.assertEqual(meta["ref"], "v1.0.0")
        self.assertEqual(meta["license"], "AGPL-3.0-only")
        self.assertTrue(meta["source_url"].endswith("/tree/" + self.sha))
        self.assertEqual(meta["archive_sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_archive_contents(self):
        run(self.repo, "v1.0.0", str(self.tmp / "out"))
        with tarfile.open(self.tmp / "out/producto-core-v1.0.0.tar.gz") as tar:
            names = tar.getnames()
        self.assertIn("producto-core-v1.0.0/LICENSE", names)
        self.assertIn("producto-core-v1.0.0/main.py", names)
        self.assertFalse(any("/.git/" in n for n in names))

    def test_untracked_files_are_excluded(self):
        (self.repo / "secret.env").write_text("TOKEN=not-real\n")
        run(self.repo, "v1.0.0", str(self.tmp / "out"))
        with tarfile.open(self.tmp / "out/producto-core-v1.0.0.tar.gz") as tar:
            self.assertNotIn("producto-core-v1.0.0/secret.env", tar.getnames())

    def test_non_tag_ref_uses_short_commit(self):
        run(self.repo, "HEAD", str(self.tmp / "out"))
        self.assertTrue((self.tmp / f"out/producto-core-{self.sha[:12]}.tar.gz").exists())

    def test_unknown_ref_fails(self):
        with self.assertRaises(subprocess.CalledProcessError):
            run(self.repo, "does-not-exist", str(self.tmp / "out"))

    def test_invalid_label_fails(self):
        with self.assertRaises(subprocess.CalledProcessError):
            run(self.repo, "HEAD", str(self.tmp / "out"), "bad/label")


if __name__ == "__main__":
    unittest.main()
