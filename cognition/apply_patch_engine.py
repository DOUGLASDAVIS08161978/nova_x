#!/usr/bin/env python3
"""
Nova-X Apply Patch Engine

Provides safe file writing, syntax validation,
git commit/push helpers, and utilities for the
autonomous patch pipeline.
"""

import ast
import subprocess
from pathlib import Path


class ApplyPatchEngine:

    def validate_python(self, filename: str, source: str):
        """Validate Python syntax before writing."""
        try:
            ast.parse(source)
            return True, None
        except SyntaxError as e:
            return False, str(e)

    def write_file(self, filename: str, source: str):
        """Safely overwrite a file."""
        path = Path(filename)
        path.write_text(source, encoding="utf-8")

    def stage_all(self):
        subprocess.run(["git", "add", "-A"], check=True)

    def has_staged_changes(self):
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"]
        )
        return result.returncode != 0

    def commit(self, message):
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True
        )

    def push(self, branch):
        subprocess.run(
            ["git", "push", "-u", "origin", branch],
            check=True
        )

    def current_branch(self):
        return subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True
        ).strip()


if __name__ == "__main__":
    print("ApplyPatchEngine ready.")
