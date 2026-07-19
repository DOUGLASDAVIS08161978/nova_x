#!/usr/bin/env python3
"""
===========================================================
NOVA-X Cognitive Cycle Engine v1.0
===========================================================

Coordinates the internal cognitive loop.

Cycle:

Observe
Remember
Reflect
Plan
Improve
Rest

Future:
- Autonomous scheduling
- Goal prioritization
- Experiment execution
- Reflection scoring
- Multi-engine reasoning
===========================================================
"""

from datetime import datetime
import time

from memory.episodic_memory import EpisodicMemory
from cognition.self_improvement import SelfImprovementPlanner


class CognitiveCycle:

    def __init__(self):

        self.memory = EpisodicMemory()

        self.planner = SelfImprovementPlanner()

        self.cycles = 0

        self.running = False


    def observe(self):

        print("[Observe] Reviewing recent memories...")

        recent = self.memory.recent(5)

        print(f"[Observe] {len(recent)} memories available.")

        return recent


    def reflect(self, memories):

        print("[Reflect] Looking for patterns...")

        successful = sum(
            1 for m in memories
            if m.get("success", False)
        )

        failed = len(memories) - successful

        print(
            f"[Reflect] Success={successful} Failure={failed}"
        )

        return {

            "successful": successful,

            "failed": failed

        }


    def plan(self, reflection):

        print("[Plan] Generating improvement proposal...")

        if reflection["failed"] > 0:

            proposal = self.planner.propose(

                "Reduce Failures",

                "Investigate unsuccessful reasoning events.",

                priority="High"

            )

        else:

            proposal = self.planner.propose(

                "Improve Knowledge",

                "Continue expanding reasoning capability.",

                priority="Medium"

            )

        print("[Plan] Proposal created.")

        return proposal


    def remember(self, proposal):

        self.memory.remember(

            event="self_improvement",

            prompt=proposal["title"],

            response=proposal["description"],

            engine="planner",

            success=True,

            metadata=proposal

        )


    def cycle(self):

        print("\n" + "=" * 55)

        print(
            f"COGNITIVE CYCLE {self.cycles+1}"
        )

        print("=" * 55)

        memories = self.observe()

        reflection = self.reflect(memories)

        proposal = self.plan(reflection)

        self.remember(proposal)

        self.cycles += 1

        print("[Cycle] Complete.")


    def run(self,
            cycles=3,
            delay=2):

        self.running = True

        while self.running and self.cycles < cycles:

            self.cycle()

            time.sleep(delay)

        print("\nCognitive cycle finished.")


if __name__ == "__main__":

    engine = CognitiveCycle()

    engine.run()
