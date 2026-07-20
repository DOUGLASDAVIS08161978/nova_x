#!/usr/bin/env python3
"""
===========================================================
NOVA-X Module Registry v1.0
===========================================================

Registers and manages NOVA-X execution modules.

Author:
Douglas Davis & OpenAI
===========================================================
"""

from datetime import datetime


class ModuleRegistry:

    def __init__(self):

        self.modules = {}

    def register(self, name, version="1.0", enabled=True, description=""):

        self.modules[name] = {
            "version": version,
            "enabled": enabled,
            "description": description,
            "registered": datetime.now().isoformat(timespec="seconds")
        }

    def enable(self, name):

        if name in self.modules:
            self.modules[name]["enabled"] = True

    def disable(self, name):

        if name in self.modules:
            self.modules[name]["enabled"] = False

    def enabled_modules(self):

        return {
            name: info
            for name, info in self.modules.items()
            if info["enabled"]
        }

    def all_modules(self):

        return self.modules

    def summary(self):

        total = len(self.modules)
        enabled = len(self.enabled_modules())

        return {
            "total_modules": total,
            "enabled_modules": enabled,
            "disabled_modules": total - enabled
        }


############################################################

if __name__ == "__main__":

    registry = ModuleRegistry()

    registry.register(
        "Task Planner",
        description="Creates execution plans."
    )

    registry.register(
        "Task Executor",
        description="Executes planned tasks."
    )

    registry.register(
        "Execution History",
        description="Stores previous runs."
    )

    registry.register(
        "Self Evaluation",
        description="Evaluates execution quality."
    )

    registry.register(
        "Capability Analyzer",
        description="Finds missing capabilities."
    )

    registry.register(
        "Tool Architect",
        description="Designs new tools."
    )

    registry.register(
        "Tool Generator",
        description="Generates tool scaffolds."
    )

    registry.register(
        "Innovation Queue",
        description="Tracks future ideas."
    )

    registry.disable("Execution History")

    print()
    print("=" * 60)
    print("NOVA-X MODULE REGISTRY")
    print("=" * 60)
    print()

    for name, info in registry.all_modules().items():

        status = "ENABLED" if info["enabled"] else "DISABLED"

        print(f"{status:9} | {name}")

    print()
    print("=" * 60)

    for key, value in registry.summary().items():

        print(f"{key:20}: {value}")
