#!/usr/bin/env python3
"""
===========================================================
NOVA-X Learning Cycle v2.0
===========================================================

Complete autonomous learning pipeline.

Stages
------
1. Curiosity
2. Research
3. Knowledge Import
4. Reflection
5. Learning Summary

===========================================================
"""

from core.global_workspace import GlobalWorkspace

from cognition.curiosity_engine import CuriosityEngine
from cognition.research_engine import ResearchEngine
from cognition.research_knowledge_bridge import ResearchKnowledgeBridge
from cognition.reflection_engine import ReflectionEngine


class LearningCycle:

    def __init__(self):

        self.workspace = GlobalWorkspace()

        self.curiosity = CuriosityEngine(self.workspace)
        self.research = ResearchEngine(self.workspace)
        self.bridge = ResearchKnowledgeBridge()
        self.reflection = ReflectionEngine(self.workspace)

    def run(self):

        print()
        print("======================================")
        print("      NOVA-X LEARNING CYCLE v2.0")
        print("======================================")

        #
        # STEP 1
        #

        print("\n[1] Curiosity")

        request = self.curiosity.create_research_request()

        if request is None:

            print("No topic selected.")
            return

        topic = request["topic"]

        print("Topic:", topic)

        #
        # STEP 2
        #

        print("\n[2] Research")

        self.research.process()

        results = self.workspace.get_category(
            "research_result"
        )

        if not results:

            print("No research produced.")
            return

        latest = results[-1]

        #
        # STEP 3
        #

        print("\n[3] Updating Knowledge Graph")

        self.bridge.import_research(

            topic,

            latest["message"]

        )

        #
        # STEP 4
        #

        print("\n[4] Reflection")

        self.reflection.reflect()

        #
        # STEP 5
        #

        print("\n[5] Learning Summary")

        print("----------------------")

        print("Topic:")
        print(topic)

        print()

        print("Research Source:")
        print(
            latest["metadata"].get(
                "source",
                "unknown"
            )
        )

        print()

        print("Knowledge successfully updated.")

        print()

        print("Cycle Complete.")

        print()

        print("Workspace Events")

        print("----------------")

        for event in self.workspace.get_events():

            print(event)


if __name__ == "__main__":

    LearningCycle().run()

