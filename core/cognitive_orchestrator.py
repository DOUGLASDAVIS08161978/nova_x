#!/usr/bin/env python3
"""
===========================================================
NOVA-X Cognitive Orchestrator v2.0
===========================================================

Integrated Cognitive Runtime

Connects:
- Reasoning Manager (Groq)
- Episodic Memory
- Goal Manager
- Self Improvement Planner

===========================================================
"""

import time
from datetime import datetime

from memory.episodic_memory import EpisodicMemory
from core.reasoning_manager import ReasoningManager
from cognition.self_improvement import SelfImprovementPlanner
from cognition.goal_manager import GoalManager


class CognitiveOrchestrator:

    def __init__(self):

        print("[Orchestrator] Starting NOVA-X systems...")

        self.memory = EpisodicMemory()

        self.reasoner = ReasoningManager()

        self.improvement = SelfImprovementPlanner()

        self.goals = GoalManager()

        self.cycles = 0

        print("[Orchestrator] All systems online.\n")


    def observe(self):

        memories = self.memory.recent(5)

        goals = self.goals.active_goals()

        print("[Observe]")
        print(f" Memories: {len(memories)}")
        print(f" Active Goals: {len(goals)}")

        return memories, goals


    def reason(self, memories, goals):

        print("[Reasoning via Groq]")

        prompt = f"""
You are the reasoning engine inside NOVA-X.

Analyze the current system state.

Recent memories:
{memories}

Current goals:
{goals}

Suggest one practical improvement.
"""

        result = self.reasoner.reason(prompt)

        if result["success"]:

            return result["response"]

        return "No reasoning result."


    def improve(self, suggestion):

        print("[Improvement Planner]")

        proposal = self.improvement.propose(

            title="Architecture Enhancement",

            description=suggestion,

            priority="Medium"

        )

        return proposal


    def remember(self, proposal):

        print("[Memory] Saving experience")

        self.memory.remember(

            event="cognitive_cycle",

            prompt=proposal["title"],

            response=proposal["description"],

            engine="groq",

            success=True,

            metadata=proposal

        )


    def run_cycle(self):

        self.cycles += 1

        print("\n" + "="*60)
        print(f"NOVA-X COGNITIVE CYCLE {self.cycles}")
        print("="*60)


        memories, goals = self.observe()

        suggestion = self.reason(
            memories,
            goals
        )

        print("\nGroq Suggestion:")
        print(suggestion[:500])


        proposal = self.improve(
            suggestion
        )

        self.remember(
            proposal
        )


        print("\nCycle Complete.")


    def run(self, cycles=3):

        for _ in range(cycles):

            self.run_cycle()

            time.sleep(3)


if __name__ == "__main__":

    system = CognitiveOrchestrator()

    system.run()
