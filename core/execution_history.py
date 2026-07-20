#!/usr/bin/env python3
"""
===========================================================
NOVA-X Execution History v1.0
===========================================================

Stores completed executions so NOVA-X can review
what she has accomplished.

Author:
Douglas Davis & OpenAI

===========================================================
"""

import json
import os
from datetime import datetime


class ExecutionHistory:

    def __init__(self, filename="execution_history.json"):

        self.filename = filename

        if not os.path.exists(self.filename):

            with open(self.filename, "w") as f:
                json.dump([], f, indent=4)

    def _load(self):

        with open(self.filename, "r") as f:
            return json.load(f)

    def _save(self, history):

        with open(self.filename, "w") as f:
            json.dump(history, f, indent=4)

    def record(self, goal, report):

        history = self._load()

        entry = {

            "timestamp": datetime.now().isoformat(timespec="seconds"),

            "goal": goal,

            "successes": sum(
                1 for r in report["results"]
                if r["status"] == "SUCCESS"
            ),

            "total_steps": len(report["results"]),

            "report": report

        }

        history.append(entry)

        self._save(history)

        return entry

    def summary(self):

        history = self._load()

        print()

        print("=" * 60)
        print("NOVA-X EXECUTION HISTORY")
        print("=" * 60)

        print()

        print("Total Executions:", len(history))

        print()

        for i, item in enumerate(history, 1):

            print(f"{i}. {item['timestamp']}")

            print(" Goal :", item["goal"])

            print(
                f" Success : {item['successes']}/{item['total_steps']}"
            )

            print()

        return history


############################################################

if __name__ == "__main__":

    sample_report = {

        "results": [

            {"status": "SUCCESS"},

            {"status": "SUCCESS"},

            {"status": "SUCCESS"}

        ]

    }

    history = ExecutionHistory()

    history.record(

        "Run a Python experiment then open GitHub",

        sample_report

    )

    history.summary()

