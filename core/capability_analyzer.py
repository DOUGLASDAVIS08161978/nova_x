#!/usr/bin/env python3
"""
===========================================================
NOVA-X Capability Analyzer v1.0
===========================================================

Detects capability gaps and proposes new tools.

Author:
Douglas Davis & OpenAI
===========================================================
"""

from tool_registry import ToolRegistry


class CapabilityAnalyzer:

    def __init__(self, registry):
        self.registry = registry

    def analyze(self, goal):

        goal_lower = goal.lower()

        if (
            "python" in goal_lower
            and self.registry.has("Code Executor")
        ):
            return {"status": "AVAILABLE"}

        if (
            "experiment" in goal_lower
            and self.registry.has("Experiment Engine")
        ):
            return {"status": "AVAILABLE"}

        if (
            "github" in goal_lower
            and self.registry.has("Android Agent")
        ):
            return {"status": "AVAILABLE"}

        return {
            "status": "MISSING",
            "proposal": self.propose_tool(goal)
        }

    def propose_tool(self, goal):

        goal_lower = goal.lower()

        if "pdf" in goal_lower:
            return {
                "name": "PDF Reader",
                "purpose": "Extract text from PDF files.",
                "confidence": 0.95
            }

        if "image" in goal_lower:
            return {
                "name": "Image Analyzer",
                "purpose": "Analyze images and extract information.",
                "confidence": 0.92
            }

        return {
            "name": "Custom Tool",
            "purpose": f"Support goal: {goal}",
            "confidence": 0.60
        }


############################################################

if __name__ == "__main__":

    registry = ToolRegistry()

    class Dummy:
        pass

    registry.register("Code Executor", Dummy())
    registry.register("Experiment Engine", Dummy())
    registry.register("Android Agent", Dummy())

    analyzer = CapabilityAnalyzer(registry)

    goals = [

        "Run Python code",

        "Analyze a PDF",

        "Open GitHub"

    ]

    for goal in goals:

        print()
        print("=" * 55)

        print("Goal:", goal)

        result = analyzer.analyze(goal)

        if result["status"] == "AVAILABLE":

            print("Capability: AVAILABLE")

        else:

            print("Capability: MISSING")

            proposal = result["proposal"]

            print("Suggested Tool :", proposal["name"])

            print("Purpose        :", proposal["purpose"])

            print(
                "Confidence     :",
                f"{proposal['confidence']:.0%}"
            )

