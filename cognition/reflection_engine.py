#!/usr/bin/env python3
"""
===========================================================
NOVA-X Reflection Engine v1.0
===========================================================

Reviews recent research and generates reflections.

Current Version
---------------
- Reads research results
- Produces observations
- Suggests follow-up questions
- Publishes reflections into the Workspace

Future
------
- Contradiction detection
- Belief revision
- Confidence scoring
- Learning metrics
===========================================================
"""

from core.global_workspace import GlobalWorkspace


class ReflectionEngine:

    def __init__(self, workspace):

        self.workspace = workspace


    def reflect(self):

        research = self.workspace.get_category(
            "research_result"
        )

        if not research:

            print("No research results to reflect on.")
            return

        latest = research[-1]

        topic = latest["metadata"].get(
            "topic",
            latest["message"]
        )

        message = latest["message"]

        words = len(message.split())

        reflection = (
            f"Research on '{topic}' produced "
            f"{words} words of information."
        )

        follow_up = (
            f"What additional topics are closely "
            f"related to {topic}?"
        )

        self.workspace.broadcast(

            "ReflectionEngine",

            reflection,

            category="reflection",

            priority=0.75,

            metadata={

                "topic": topic,

                "word_count": words,

                "follow_up": follow_up

            }

        )

        print()
        print("Reflection")
        print("----------")
        print(reflection)
        print()
        print("Suggested Follow-up")
        print("-------------------")
        print(follow_up)
        print()


if __name__ == "__main__":

    workspace = GlobalWorkspace()

    workspace.broadcast(

        "ResearchEngine",

        "Nikola Tesla was a Serbian-American inventor "
        "best known for alternating current.",

        category="research_result",

        metadata={

            "topic": "Nikola Tesla"

        }

    )

    engine = ReflectionEngine(
        workspace
    )

    engine.reflect()

    print()

    print("Workspace Events")
    print("----------------")

    for event in workspace.get_events():

        print(event)

