#!/usr/bin/env python3
"""
===========================================================
NOVA-X Consistency Checker v2.0
===========================================================

Checks the Global Workspace for duplicate messages and
simple opposite-word contradictions.

Designed for the current NOVA-X GlobalWorkspace.
===========================================================
"""

import re

from core.global_workspace import GlobalWorkspace


OPPOSITES = [

    ("increase", "decrease"),
    ("rise", "fall"),
    ("true", "false"),
    ("success", "failure"),
    ("high", "low"),
    ("positive", "negative"),
    ("enable", "disable"),
    ("allow", "deny")

]


class ConsistencyChecker:

    def __init__(self, workspace):

        self.workspace = workspace

        self.flags = []


    def check(self):

        events = self.workspace.get_events()

        self.flags = []

        for i in range(len(events)):

            for j in range(i + 1, len(events)):

                a = events[i]

                b = events[j]

                msg_a = a["message"].lower()

                msg_b = b["message"].lower()


                if msg_a == msg_b:

                    self.flags.append({

                        "type": "duplicate",

                        "a": a,

                        "b": b

                    })


                for word1, word2 in OPPOSITES:

                    cond1 = word1 in msg_a and word2 in msg_b

                    cond2 = word2 in msg_a and word1 in msg_b

                    if cond1 or cond2:

                        self.flags.append({

                            "type": "contradiction",

                            "reason": f"{word1} vs {word2}",

                            "a": a,

                            "b": b

                        })


        return self.flags


    def publish_results(self):

        results = self.check()

        for result in results:

            self.workspace.broadcast(

                "ConsistencyChecker",

                f"Flagged {result['type']}"

            )

        return len(results)


if __name__ == "__main__":

    workspace = GlobalWorkspace()

    workspace.broadcast(

        "Reasoner",

        "Prices will rise next quarter."

    )

    workspace.broadcast(

        "Planner",

        "Prices will fall next quarter."

    )

    checker = ConsistencyChecker(

        workspace

    )

    count = checker.publish_results()

    print()

    print(f"{count} issue(s) found.")

    print()

    for flag in checker.flags:

        print(flag)
