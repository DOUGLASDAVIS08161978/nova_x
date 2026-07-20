#!/usr/bin/env python3
"""
============================================================
NOVA-X Reflection Engine v2.0
============================================================

Evaluates completed work and records engineering lessons.

Douglas Davis & OpenAI
============================================================
"""

from datetime import datetime
import json
from pathlib import Path


REFLECTION_FILE = Path("reflection_log.json")


class ReflectionEngine:

    def __init__(self):

        self.timestamp = datetime.now().isoformat(timespec="seconds")

    def reflect(
        self,
        goal,
        outcome,
        confidence,
        evidence,
        improvements
    ):

        return {

            "timestamp": self.timestamp,

            "goal": goal,

            "outcome": outcome,

            "confidence": confidence,

            "evidence": evidence,

            "next_improvements": improvements

        }

    def save(self, reflection):

        history = []

        if REFLECTION_FILE.exists():

            try:

                history = json.loads(
                    REFLECTION_FILE.read_text()
                )

            except Exception:

                history = []

        history.append(reflection)

        REFLECTION_FILE.write_text(

            json.dumps(
                history,
                indent=4
            )

        )

    def print_report(self, reflection):

        print()
        print("=" * 60)
        print("NOVA-X REFLECTION REPORT")
        print("=" * 60)

        print()

        print("Goal:")
        print(reflection["goal"])

        print()

        print("Outcome:")
        print(reflection["outcome"])

        print()

        print(
            f"Confidence: {reflection['confidence']:.2f}"
        )

        print()

        print("Evidence:")

        for item in reflection["evidence"]:

            print("  ✓", item)

        print()

        print("Next Improvements:")

        for item in reflection["next_improvements"]:

            print("  •", item)

        print()


############################################################

if __name__ == "__main__":

    engine = ReflectionEngine()

    report = engine.reflect(

        goal="Integrate Module Registry",

        outcome="Successful integration.",

        confidence=0.96,

        evidence=[

            "Registry loaded.",

            "Pipeline executed.",

            "No runtime errors."

        ],

        improvements=[

            "Support dynamic module discovery.",

            "Integrate execution metrics."

        ]

    )

    engine.save(report)

    engine.print_report(report)

    print("Reflection saved to reflection_log.json")
