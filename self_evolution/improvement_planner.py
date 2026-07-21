#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
NOVA X IMPROVEMENT PLANNER v1.0
Human-in-the-Loop Engineering Planner
═══════════════════════════════════════════════════════════════════════

Reads:
    opportunity_backlog.json
    project_knowledge_graph.json

Produces:
    improvement_plan.json

This module NEVER edits source code.
"""

from pathlib import Path
from datetime import datetime, UTC
import json

REPORT_DIR = Path("self_evolution/reports")

BACKLOG = REPORT_DIR / "opportunity_backlog.json"
GRAPH = REPORT_DIR / "project_knowledge_graph.json"
OUTPUT = REPORT_DIR / "improvement_plan.json"


class ImprovementPlanner:

    def __init__(self):
        self.tasks = []

    def load_json(self, path):

        if not path.exists():
            raise FileNotFoundError(path)

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def confidence(self, priority):

        if priority >= 95:
            return 0.97
        elif priority >= 90:
            return 0.93
        elif priority >= 80:
            return 0.88
        elif priority >= 70:
            return 0.80

        return 0.72

    def risk(self, item):

        title = item["title"].lower()

        if "parser" in title:
            return "High"

        if "refactor" in title:
            return "Medium"

        return "Low"

    def effort(self, item):

        p = item["priority"]

        if p >= 95:
            return "Large"

        if p >= 80:
            return "Medium"

        return "Small"

    def affected_modules(self, graph, title):

        matches = []

        words = title.lower().split()

        for module in graph.get("modules", []):

            filename = module.get("file", "").lower()

            if any(word in filename for word in words):
                matches.append(module["file"])

        return matches

    def plan(self):

        backlog = self.load_json(BACKLOG)
        graph = self.load_json(GRAPH)

        for item in backlog["items"]:

            self.tasks.append({

                "title": item["title"],

                "priority": item["priority"],

                "confidence":
                    self.confidence(item["priority"]),

                "risk":
                    self.risk(item),

                "estimated_effort":
                    self.effort(item),

                "category":
                    item["category"],

                "reason":
                    item["evidence"],

                "affected_modules":
                    self.affected_modules(
                        graph,
                        item["title"]
                    ),

                "next_action":
                    "Generate candidate patch",

                "requires_human_review":
                    True
            })

        self.tasks.sort(
            key=lambda x: (
                x["priority"],
                x["confidence"]
            ),
            reverse=True
        )

        return {
            "generated":
                datetime.now(UTC).isoformat(),

            "planner":
                "Nova X Improvement Planner v1.0",

            "tasks":
                self.tasks
        }

    def save(self):

        plan = self.plan()

        OUTPUT.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            OUTPUT,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                plan,
                f,
                indent=4
            )

        return plan


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
"""
Auto-generated docstring for main.
"""

    try:

        planner = ImprovementPlanner()

        plan = planner.save()

    except FileNotFoundError as exc:

        print()
        print("Missing prerequisite:")
        print(exc)
        print()
        print("Run these first:")
        print("python3 self_evolution/introspection.py")
        print("python3 self_evolution/opportunity_analyzer.py")
        print("python3 self_evolution/project_knowledge_graph.py")
        print()
        return

    print()
    print("=" * 60)
    print("NOVA X IMPROVEMENT PLAN")
    print("=" * 60)
    print()

    for task in plan["tasks"][:15]:

        print(
            f"[{task['priority']:02}] "
            f"{task['title']}"
        )

        print(
            f"     Confidence : "
            f"{task['confidence']:.2f}"
        )

        print(
            f"     Risk       : "
            f"{task['risk']}"
        )

        print(
            f"     Effort     : "
            f"{task['estimated_effort']}"
        )

        print()

    print(
        f"Total Planned Tasks : "
        f"{len(plan['tasks'])}"
    )

    print(
        f"Saved Plan          : "
        f"{OUTPUT}"
    )

    print()


if __name__ == "__main__":
    main()

