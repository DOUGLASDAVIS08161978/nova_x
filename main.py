#!/usr/bin/env python3
"""
<<<<<<< Updated upstream
NOVA-X Boot Kernel v3.0 — Clean /evolve routing
"""

import os
import sys
import threading
=======
NOVA-X Boot Kernel v4.0 — Hot‑Reload + Reliable /evolve
"""

import os, sys, threading, time, importlib, pkgutil
>>>>>>> Stashed changes
from datetime import datetime
from pathlib import Path

from core.executive_controller import ExecutiveController
from memory.working_memory import WorkingMemory
from core.global_workspace import GlobalWorkspace
from cognition.identity_core import IdentityCore
from core.plugin_manager import PluginManager
from core.reasoning_manager import ReasoningManager
from core.living_cycle_daemon import LivingCycleDaemon
from core.capability_router import is_capability_question, capability_response

<<<<<<< Updated upstream
# Evolution engine v8
try:
    from cognition.patch_synthesis_engine_v8 import GitCurlEngine
    EVOLUTION_AVAILABLE = True
except ImportError:
    EVOLUTION_AVAILABLE = False
    print("⚠️  Evolution engine not found (cognition/patch_synthesis_engine_v8.py)")
=======
# Evolution engine
try:
    from cognition import patch_synthesis_engine_v8 as evolution
    EVOLUTION_AVAILABLE = True
except ImportError:
    EVOLUTION_AVAILABLE = False
    print("⚠️  Evolution engine not found.")
>>>>>>> Stashed changes


class NovaX:
    def __init__(self):
        print("=" * 55)
<<<<<<< Updated upstream
        print("          NOVA-X BOOT KERNEL v3.0")
=======
        print("          NOVA-X BOOT KERNEL v4.0")
>>>>>>> Stashed changes
        print("=" * 55)
        print()

        self.boot_time = datetime.now()
        self.modules_path = Path("modules")
        self.modules_path.mkdir(exist_ok=True)

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
<<<<<<< Updated upstream
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
=======
            if not self.groq_key:    print("      - GROQ_API_KEY not set")
            if not self.github_token: print("      - GITHUB_TOKEN not set")
            if not self.github_repo:  print("      - GITHUB_REPO not set")
            if not EVOLUTION_AVAILABLE: print("      - evolution module not found")

        print("\nSystem Ready.")
        print("Type /evolve to trigger evolution cycle.")
        print("Type /reload to hot‑reload new modules.")
        print("Type /status for system state.\n")

        # Start hot‑reload watcher
        self._start_watcher()

    def _start_watcher(self):
        """Watch the modules/ directory for changes and reload."""
        def watcher():
            last_mtime = {}
            while True:
                for py_file in self.modules_path.glob("*.py"):
                    mtime = py_file.stat().st_mtime
                    if py_file.name not in last_mtime:
                        last_mtime[py_file.name] = mtime
                    elif mtime > last_mtime[py_file.name]:
                        last_mtime[py_file.name] = mtime
                        # Reload the module
                        module_name = py_file.stem
                        try:
                            if module_name in sys.modules:
                                importlib.reload(sys.modules[module_name])
                                print(f"♻️  Hot‑reloaded: {module_name}")
                            else:
                                spec = importlib.util.spec_from_file_location(module_name, py_file)
                                if spec:
                                    mod = importlib.util.module_from_spec(spec)
                                    sys.modules[module_name] = mod
                                    spec.loader.exec_module(mod)
                                    print(f"🔌 Loaded new module: {module_name}")
                        except Exception as e:
                            print(f"⚠️  Failed to reload {module_name}: {e}")
                time.sleep(3)
        threading.Thread(target=watcher, daemon=True).start()

    def _run_evolution(self):
        print("\n🧠 EVOLUTION CYCLE STARTED")
        try:
            engine = evolution.GitCurlEngine()
            engine.run_evolution()
        except Exception as e:
            print(f"❌ Evolution cycle failed: {e}")

    def _reload_all(self):
        print("\n♻️  Reloading all modules...")
        for name, mod in list(sys.modules.items()):
            if name.startswith("modules."):
                try:
                    importlib.reload(mod)
                    print(f"   Reloaded {name}")
                except Exception as e:
                    print(f"   Failed to reload {name}: {e}")
        print("✅ Reload complete.")
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======
            elif cmd == "/reload":
                self._reload_all()
                return
>>>>>>> Stashed changes
            elif cmd == "/status":
                print("\n📊 Nova-X Status:")
                print(f"  Boot time: {self.boot_time.isoformat()}")
                print(f"  Groq API: {'✅' if self.groq_key else '❌'}")
                print(f"  GitHub token: {'✅' if self.github_token else '❌'}")
                print(f"  GitHub repo: {self.github_repo or 'Not set'}")
                print(f"  Evolution module: {'✅' if EVOLUTION_AVAILABLE else '❌'}")
<<<<<<< Updated upstream
=======
                print(f"  Loaded modules: {', '.join([m for m in sys.modules if m.startswith('modules.')]) or 'None'}")
>>>>>>> Stashed changes
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
