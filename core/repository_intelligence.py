#!/usr/bin/env python3
"""
============================================================
NOVA-X Repository Intelligence Engine v1.0
============================================================

Scans the NOVA-X repository and builds an architectural
inventory to guide future development.

Douglas Davis & OpenAI
============================================================
"""

import os
import ast
import json
from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "nova_x"
INDEX_FILE = ROOT / "repository_index.json"


class RepositoryIntelligence:

    def __init__(self):

        self.timestamp = datetime.now().isoformat(timespec="seconds")
        self.index = {
            "timestamp": self.timestamp,
            "files": []
        }

    def scan(self):

        for root, dirs, files in os.walk(ROOT):

            dirs[:] = [
                d for d in dirs
                if d not in (
                    "__pycache__",
                    ".git",
                    ".venv",
                    "venv"
                )
            ]

            for file in files:

                if not file.endswith(".py"):
                    continue

                path = Path(root) / file

                self.index["files"].append(
                    self.analyze(path)
                )

    def analyze(self, path):

        info = {
            "file": str(path.relative_to(ROOT)),
            "classes": [],
            "functions": []
        }

        try:

            tree = ast.parse(path.read_text())

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):
                    info["classes"].append(node.name)

                elif isinstance(node, ast.FunctionDef):
                    info["functions"].append(node.name)

        except Exception as e:

            info["error"] = str(e)

        return info

    def save(self):

        INDEX_FILE.write_text(
            json.dumps(self.index, indent=4)
        )

    def print_report(self):

        print()
        print("=" * 60)
        print("NOVA-X REPOSITORY INTELLIGENCE REPORT")
        print("=" * 60)
        print()

        total_files = len(self.index["files"])
        total_classes = 0
        total_functions = 0

        for file in self.index["files"]:

            print(file["file"])

            if file["classes"]:
                print("  Classes:")
                for c in file["classes"]:
                    print("    •", c)

            if file["functions"]:
                print("  Functions:")
                for f in file["functions"]:
                    print("    •", f)

            if "error" in file:
                print("  Parse Error:", file["error"])

            total_classes += len(file["classes"])
            total_functions += len(file["functions"])

            print()

        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)

        print("Python Files :", total_files)
        print("Classes      :", total_classes)
        print("Functions    :", total_functions)

        print()
        print("Repository index saved to")
        print(INDEX_FILE)

        print()
        print("Future capabilities:")
        print(" ✓ Duplicate detection")
        print(" ✓ Dependency graph")
        print(" ✓ Module recommendations")
        print(" ✓ Pull request suggestions")
        print(" ✓ Architecture visualization")


############################################################

if __name__ == "__main__":

    engine = RepositoryIntelligence()

    engine.scan()

    engine.save()

    engine.print_report()

