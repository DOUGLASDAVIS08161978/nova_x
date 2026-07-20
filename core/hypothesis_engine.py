#!/usr/bin/env python3
"""
============================================================
NOVA-X Hypothesis Engine v1.0
============================================================

Generates multiple competing hypotheses instead of
committing immediately to a single explanation.

Douglas Davis & OpenAI
============================================================
"""

from datetime import datetime
import json
from pathlib import Path

LOG_FILE = Path("hypothesis_log.json")


class HypothesisEngine:

    def __init__(self):
        self.timestamp = datetime.now().isoformat(timespec="seconds")

    def evaluate(self, problem, hypotheses):

        total = sum(h["confidence"] for h in hypotheses)

        if total > 0:
            for h in hypotheses:
                h["normalized_confidence"] = round(
                    h["confidence"] / total,
                    3
                )

        ranked = sorted(
            hypotheses,
            key=lambda x: x["normalized_confidence"],
            reverse=True
        )

        return {
            "timestamp": self.timestamp,
            "problem": problem,
            "hypotheses": ranked
        }

    def save(self, report):

        history = []

        if LOG_FILE.exists():

            try:
                history = json.loads(LOG_FILE.read_text())
            except Exception:
                history = []

        history.append(report)

        LOG_FILE.write_text(
            json.dumps(history, indent=4)
        )

    def print_report(self, report):

        print()
        print("=" * 60)
        print("NOVA-X HYPOTHESIS REPORT")
        print("=" * 60)
        print()

        print("Problem:")
        print(report["problem"])
        print()

        for i, hypothesis in enumerate(report["hypotheses"], start=1):

            print(f"Hypothesis {i}")
            print("-" * 40)
            print("Explanation:")
            print(hypothesis["description"])
            print()

            print(
                "Confidence:",
                hypothesis["normalized_confidence"]
            )

            print()

            print("Evidence:")

            for item in hypothesis["evidence"]:
                print("  ✓", item)

            print()

            print("Suggested Test:")
            print(hypothesis["test"])

            print()

        print("=" * 60)


############################################################

if __name__ == "__main__":

    engine = HypothesisEngine()

    report = engine.evaluate(

        problem="Battery will not begin charging immediately.",

        hypotheses=[

            {
                "description":
                "Battery temperature is too high.",

                "confidence":0.70,

                "evidence":[
                    "Battery recently used.",
                    "Battery feels warm."
                ],

                "test":
                "Allow battery to cool for 30 minutes."
            },

            {
                "description":
                "Battery Management System balancing cells.",

                "confidence":0.20,

                "evidence":[
                    "Charger indicates standby."
                ],

                "test":
                "Leave charger connected for one hour."
            },

            {
                "description":
                "Faulty charger.",

                "confidence":0.10,

                "evidence":[
                    "No charging LEDs."
                ],

                "test":
                "Test with another charger."
            }

        ]

    )

    engine.save(report)

    engine.print_report(report)

    print()
    print("Hypothesis log saved to hypothesis_log.json")

