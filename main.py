#!/usr/bin/env python3
"""
NOVA-X Boot Kernel v3.0 — Clean /evolve routing
"""

import os
import sys
import threading
from datetime import datetime

from core.executive_controller import ExecutiveController
from memory.working_memory import WorkingMemory
from core.global_workspace import GlobalWorkspace
from cognition.identity_core import IdentityCore
from core.plugin_manager import PluginManager
from core.reasoning_manager import ReasoningManager
from core.living_cycle_daemon import LivingCycleDaemon
from core.capability_router import is_capability_question, capability_response

# Evolution engine v8
try:
    from cognition.patch_synthesis_engine_v8 import GitCurlEngine
    EVOLUTION_AVAILABLE = True
except ImportError:
    EVOLUTION_AVAILABLE = False
    print("⚠️  Evolution engine not found (cognition/patch_synthesis_engine_v8.py)")


class NovaX:
    def __init__(self):
        print("=" * 55)
        print("          NOVA-X BOOT KERNEL v3.0")
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
            print("  (Unable to enumerate)")

        # Environment
        self.groq_key = os.environ.get("GROQ_API_KEY", "")
        self.github_token = os.environ.get("GITHUB_TOKEN", "")
        self.github_repo = os.environ.get("GITHUB_REPO", "")

        print("\n🔐 Evolution Autopilot:")
        if self.groq_key and self.github_token and self.github_repo and EVOLUTION_AVAILABLE:
            print("   ✅ Enabled (Groq + GitHub ready)")
        else:
            print("   ⏸️  Disabled (missing environment or module)")
            if not self.groq_key:
                print("      - GROQ_API_KEY not set")
            if not self.github_token:
                print("      - GITHUB_TOKEN not set")
            if not self.github_repo:
                print("      - GITHUB_REPO not set")
            if not EVOLUTION_AVAILABLE:
                print("      - evolution module not found")

        print("\nSystem Ready.")
        print("Type /evolve to trigger evolution cycle.\n")

    def _run_evolution(self):
        """Run the evolution cycle (non‑blocking)."""
        print("\n🧠 EVOLUTION CYCLE STARTED")
        try:
            engine = GitCurlEngine()
            engine.run_evolution()
        except Exception as e:
            print(f"❌ Evolution cycle failed: {e}")

    def ask(self, prompt):
        # ---- Slash commands ----
        if prompt.startswith("/"):
            cmd = prompt.strip().lower()
            if cmd == "/evolve":
                if EVOLUTION_AVAILABLE and self.groq_key and self.github_token and self.github_repo:
                    print("\n⏳ Starting evolution cycle...")
                    threading.Thread(target=self._run_evolution, daemon=True).start()
                else:
                    print("⚠️  Evolution not available. Check environment and module.")
                return
            elif cmd == "/status":
                print("\n📊 Nova-X Status:")
                print(f"  Boot time: {self.boot_time.isoformat()}")
                print(f"  Groq API: {'✅' if self.groq_key else '❌'}")
                print(f"  GitHub token: {'✅' if self.github_token else '❌'}")
                print(f"  GitHub repo: {self.github_repo or 'Not set'}")
                print(f"  Evolution module: {'✅' if EVOLUTION_AVAILABLE else '❌'}")
                return
            else:
                print(f"Unknown command: {cmd}")
                return

        # ---- Normal reasoning ----
        print("\nThinking...\n")
        if is_capability_question(prompt):
            print(capability_response())
            return

        try:
            result = self.reasoning.reason(prompt)
            if isinstance(result, str):
                print(result)
                return
            if isinstance(result, dict):
                if result.get("success", False):
                    print(result.get("response") or result.get("text") or result.get("message") or str(result))
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
                print("Unexpected result:", result)
                return
            print(result)
        except Exception as e:
            print("\nRuntime Error:")
            print(type(e).__name__, "-", e)

    def shutdown(self):
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
            if prompt.lower() in ("quit", "exit", "bye"):
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
