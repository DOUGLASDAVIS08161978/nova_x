#!/usr/bin/env python3

"""
NOVA-X Executive Controller
Version 0.1
"""

from datetime import datetime
import time


class ExecutiveController:
    def __init__(self):
        self.modules = {}
        self.running = False
        self.cycle = 0

    def register_module(self, name, module):
        self.modules[name] = module
        print(f"[+] Registered module: {name}")

    def startup(self):
        print("=" * 50)
        print("        NOVA-X Executive Controller")
        print("=" * 50)
        print(f"Startup Time: {datetime.now()}")
        print()

        if not self.modules:
            print("No modules registered.")
        else:
            print("Modules:")
            for name in self.modules:
                print(f"  - {name}")

        print()

    def run_cycle(self):
        self.cycle += 1
        print(f"\n----- Cognitive Cycle {self.cycle} -----")

        for name, module in self.modules.items():
            if hasattr(module, "update"):
                module.update()

    def run(self, cycles=5):
        self.running = True
        self.startup()

        while self.running and self.cycle < cycles:
            self.run_cycle()
            time.sleep(1)

        print("\nSystem shutdown.")


if __name__ == "__main__":
    controller = ExecutiveController()
    controller.run()
