#!/usr/bin/env python3
"""
===========================================================
NOVA-X Tool Registry v1.0
===========================================================

Central registry for NOVA-X capabilities.

Author:
Douglas Davis & OpenAI

===========================================================
"""


class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, name, tool, description=""):

        self.tools[name] = {
            "instance": tool,
            "description": description
        }

        print(f"[Registry] Registered: {name}")

    def get(self, name):

        return self.tools.get(name, {}).get("instance")

    def has(self, name):

        return name in self.tools

    def list_tools(self):

        return sorted(self.tools.keys())

    def describe(self):

        print("\n" + "=" * 55)
        print("NOVA-X TOOL REGISTRY")
        print("=" * 55)

        for name in sorted(self.tools.keys()):

            info = self.tools[name]

            print(f"\n{name}")

            if info["description"]:
                print("  ", info["description"])

        print()


###############################################################

if __name__ == "__main__":

    class Dummy:
        pass

    registry = ToolRegistry()

    registry.register(
        "Code Executor",
        Dummy(),
        "Executes Python experiments."
    )

    registry.register(
        "Experiment Engine",
        Dummy(),
        "Runs controlled software experiments."
    )

    registry.register(
        "Android Agent",
        Dummy(),
        "Interacts with Android using approved actions."
    )

    registry.describe()

    print("Available Tools:")

    for tool in registry.list_tools():

        print(" •", tool)
