#!/usr/bin/env python3
"""
============================================================
NOVA-X Startup Health Check v1.0
============================================================

Verifies that essential files and directories exist before
the runtime begins.

Douglas Davis & OpenAI
============================================================
"""

from pathlib import Path

ROOT = Path.home() / "nova_x"

CHECKS = [
    ("Main Program", ROOT / "main.py"),
    ("Core Directory", ROOT / "core"),
    ("Cognition Directory", ROOT / "cognition"),
    ("Memory Directory", ROOT / "memory"),
    ("Plugins Directory", ROOT / "plugins"),
    ("Sensors Directory", ROOT / "sensors"),
    ("Daemon Directory", ROOT / "daemon"),
    ("Capability Registry", ROOT / "capability_registry.json"),
    ("Repository Index", ROOT / "repository_index.json"),
]

class StartupHealthCheck:

    def __init__(self):
        self.results = []

    def run(self):

        for name, path in CHECKS:

            ok = path.exists()

            self.results.append({
                "name": name,
                "path": str(path),
                "status": ok
            })

    def passed(self):
        return all(item["status"] for item in self.results)

    def report(self):

        print()
        print("=" * 60)
        print("NOVA-X STARTUP HEALTH CHECK")
        print("=" * 60)
        print()

        for item in self.results:

            icon = "✓" if item["status"] else "✗"

            print(f"{icon} {item['name']}")
            print(f"    {item['path']}")

        print()
        print("=" * 60)

        if self.passed():
            print("SYSTEM STATUS : READY")
        else:
            print("SYSTEM STATUS : ATTENTION REQUIRED")

        print("=" * 60)


if __name__ == "__main__":

    check = StartupHealthCheck()

    check.run()

    check.report()
