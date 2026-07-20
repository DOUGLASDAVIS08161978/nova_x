#!/usr/bin/env python3
"""
===========================================================
NOVA-X Boot Kernel v1.1
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

        try:
            for engine in self.reasoning.available_engines():
                print("  •", engine)
        except Exception:
            print("  (Unable to enumerate reasoning engines)")

        print("\nSystem Ready.")

    def ask(self, prompt):

        print("\nThinking...\n")

        try:
            result = self.reasoning.reason(prompt)

            # Plain string response
            if isinstance(result, str):
                print(result)
                return

            # Dictionary response
            if isinstance(result, dict):

                if result.get("success", False):
                    print(
                        result.get(
                            "response",
                            result.get(
                                "text",
                                result.get(
                                    "message",
                                    str(result)
                                )
                            )
                        )
                    )
                    return

                if "response" in result:
                    print(result["response"])
                    return

                if "text" in result:
                    print(result["text"])
                    return

                if "message" in result:
                    print(result["message"])
                    return

                if "error" in result:
                    print("ERROR:", result["error"])
                    return

                print("Unexpected result:")
                print(result)
                return

            print(result)

        except Exception as e:
            print("\nRuntime Error:")
            print(type(e).__name__, "-", e)


def main():

    nova = NovaX()

    while True:

        try:

            prompt = input("\nNOVA-X > ")

            if prompt.lower() in (
                "quit",
                "exit",
                "bye"
            ):
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
