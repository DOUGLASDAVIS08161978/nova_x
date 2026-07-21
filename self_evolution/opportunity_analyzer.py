#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
NOVA X OPPORTUNITY ANALYZER v1.0
Human-in-the-Loop Improvement Planning
═══════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
from datetime import datetime, UTC
import json

REPORT = Path("self_evolution/reports/introspection_report.json")
OUTPUT = Path("self_evolution/reports/opportunity_backlog.json")


class OpportunityAnalyzer:

    def __init__(self):
        self.backlog = []

    def add(self, title, priority, category, evidence):
        self.backlog.append({
            "title": title,
            "priority": priority,
            "category": category,
            "evidence": evidence,
            "status": "proposed",
            "human_review": True
        })

    def analyze(self, report):

        summary = report.get("summary", {})

        if summary.get("todos", 0):
            self.add(
                "Resolve TODO items",
                90,
                "Maintenance",
                f"{summary['todos']} TODO markers detected."
            )

        if summary.get("fixmes", 0):
            self.add(
                "Resolve FIXME items",
                95,
                "Reliability",
                f"{summary['fixmes']} FIXME markers detected."
            )

        if summary.get("long_functions", 0):
            self.add(
                "Refactor long functions",
                80,
                "Refactoring",
                f"{summary['long_functions']} functions exceed 75 lines."
            )

        for file in report.get("files", []):

            if "error" in file:
                self.add(
                    f"Repair parser issue in {file['file']}",
                    100,
                    "Parsing",
                    file["error"]
                )

            if file.get("todos", 0):
                self.add(
                    f"Review TODOs in {file['file']}",
                    60,
                    "Maintenance",
                    f"{file['todos']} TODO entries."
                )

            if file.get("fixmes", 0):
                self.add(
                    f"Review FIXMEs in {file['file']}",
                    75,
                    "Reliability",
                    f"{file['fixmes']} FIXME entries."
                )

            for fn in file.get("long_functions", []):

                self.add(
                    f"Consider refactoring {fn['name']}",
                    min(fn["length"], 99),
                    "Complexity",
                    f"{fn['length']} line function in {file['file']}"
                )

        self.backlog.sort(
            key=lambda x: x["priority"],
            reverse=True
        )

        return self.backlog


def main():
"""
Auto-generated docstring for main.
"""
"""
Auto-generated docstring for main.
"""
"""
Auto-generated docstring for main.
"""

    if not REPORT.exists():
        print("Missing introspection report.")
        print()
        print("Run:")
        print("python3 self_evolution/introspection.py")
        return

    with open(REPORT, "r", encoding="utf-8") as f:
        report = json.load(f)

    analyzer = OpportunityAnalyzer()

    backlog = analyzer.analyze(report)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(
            {
                "generated": datetime.now(UTC).isoformat(),
                "count": len(backlog),
                "items": backlog
            },
            f,
            indent=4
        )

    print()
    print("=" * 60)
    print("NOVA X OPPORTUNITY BACKLOG")
    print("=" * 60)
    print()

    for item in backlog[:20]:
        print(
            f"[{item['priority']:02}] "
            f"{item['title']}"
        )

    print()
    print(f"Total Opportunities : {len(backlog)}")
    print(f"Saved Backlog       : {OUTPUT}")
    print()


if __name__ == "__main__":
    main()

