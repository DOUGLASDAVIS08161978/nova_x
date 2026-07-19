#!/usr/bin/env python3
"""
===========================================================
NOVA-X Boot Kernel v1.0
===========================================================

Boots the NOVA-X cognitive architecture.

Current Modules:
- Executive Controller
- Working Memory
- Global Workspace
- Identity Core
- Plugin Manager
- Reasoning Manager

===========================================================
"""

from datetime import datetime

from core.executive_controller import ExecutiveController
from memory.working_memory import WorkingMemory
from core.global_workspace import GlobalWorkspace
from cognition.identity_core import IdentityCore
from core.plugin_manager import PluginManager
from core.reasoning_manager import ReasoningManager


class NovaX:

    def __init__(self):

        print("=" * 55)
        print("          NOVA-X BOOT KERNEL")
        print("=" * 55)
        print()

        self.boot_time = datetime.now()

        print("[BOOT] Executive Controller...")
        self.executive = ExecutiveController()

        print("[BOOT] Working Memory...")
        self.memory = WorkingMemory()

        print("[BOOT] Global Workspace...")
        self.workspace = GlobalWorkspace()

        print("[BOOT] Identity Core...")
        self.identity = IdentityCore()

        print("[BOOT] Plugin Manager...")
        self.plugins = PluginManager()

        print("[BOOT] Reasoning Manager...")
        self.reasoning = ReasoningManager()

        print()
        print("=" * 55)
        print("NOVA-X INITIALIZATION COMPLETE")
        print("=" * 55)

        print("\nLoaded Reasoning Engines:")

        for engine in self.reasoning.available_engines():
            print("  •", engine)

        print("\nSystem Ready.\n")


    def ask(self, prompt):

        print("\nThinking...\n")

        result = self.reasoning.reason(prompt)

        if result["success"]:
            print(result["response"])
        else:
            print(result["error"])


def main():

    nova = NovaX()

    while True:

        try:

            prompt = input("\nNOVA-X > ")

            if prompt.lower() in [
                "quit",
                "exit",
                "bye"
            ]:
                print("\nGoodbye.")
                break

            if not prompt.strip():
                continue

            nova.ask(prompt)

        except KeyboardInterrupt:

            print("\nInterrupted.")
            break


if __name__ == "__main__":
    main()
