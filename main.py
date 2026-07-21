#!/usr/bin/env python3
"""
===========================================================
NOVA-X Boot Kernel v1.3
===========================================================

Boots the NOVA-X cognitive architecture.

Current Modules:
- Executive Controller
- Working Memory
- Global Workspace
- Identity Core
- Plugin Manager
- Reasoning Manager
- Living Cycle Daemon
- Dynamic Capability Router

===========================================================
"""

from datetime import datetime

from core.executive_controller import ExecutiveController
from memory.working_memory import WorkingMemory
from core.global_workspace import GlobalWorkspace
from cognition.identity_core import IdentityCore
from core.plugin_manager import PluginManager
from core.reasoning_manager import ReasoningManager
from core.living_cycle_daemon import LivingCycleDaemon

from core.capability_router import (
    is_capability_question,
    capability_response,
)


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

        print("[BOOT] Living Cycle Daemon...")
        self.living_cycle = LivingCycleDaemon()
        self.living_cycle.start()

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

        # =====================================================
        # Dynamic Capability Routing
        # =====================================================

        if is_capability_question(prompt):
            print(capability_response())
            return

        # =====================================================
        # Normal Reasoning Pipeline
        # =====================================================

        try:

            result = self.reasoning.reason(prompt)

            if isinstance(result, str):
                print(result)
                return

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

    def shutdown(self):
        """Gracefully stop background services."""
        print("\nShutting down NOVA-X...")

        try:
            self.living_cycle.stop()
        except Exception:
            pass

        print("Shutdown complete.")


def main():

    nova = NovaX()

    while True:

        try:

            prompt = input("\nNOVA-X > ")

            if prompt.lower() in (
                "quit",
                "exit",
                "bye",
            ):
                nova.shutdown()
                print("\nGoodbye.")
                break

            if not prompt.strip():
                continue

            nova.ask(prompt)

        except KeyboardInterrupt:
            print("\nInterrupted.")
            nova.shutdown()
            break


if __name__ == "__main__":
    main()
