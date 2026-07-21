#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           NOVA-X Living Cycle Daemon v1.1                  ║
║         Background Reflection & Heartbeat Service          ║
╚══════════════════════════════════════════════════════════════╝
"""

import threading
import time
import os
from datetime import datetime


class LivingCycleDaemon:

    def __init__(self, interval=3600):

        self.interval = interval
        self.running = False
        self.thread = None
        self.cycles = 0
        self.start_time = datetime.now()

        self.base_dir = os.path.expanduser("~/nova_x")
        self.log_dir = os.path.join(self.base_dir, "logs")
        self.memory_dir = os.path.join(self.base_dir, "memory")

        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.memory_dir, exist_ok=True)

        self.log_file = os.path.join(
            self.log_dir,
            "living_cycle.log"
        )

        self.reflection_file = os.path.join(
            self.memory_dir,
            "living_reflections.txt"
        )

    def heartbeat(self):

        self.cycles += 1

        now = datetime.now()

        uptime = now - self.start_time

        stamp = now.strftime("%Y-%m-%d %H:%M:%S")

        heartbeat = (
            f"[{stamp}] "
            f"Heartbeat | "
            f"Cycle={self.cycles} | "
            f"Uptime={uptime}\n"
        )

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(heartbeat)

        print(f"[LivingCycle] Heartbeat #{self.cycles}")

    def reflect(self):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        reflection = (
            f"[{now}] "
            f"Reflection #{self.cycles}: "
            f"System operational. "
            f"Background maintenance cycle completed successfully.\n"
        )

        with open(self.reflection_file, "a", encoding="utf-8") as f:
            f.write(reflection)

        print("[LivingCycle] Reflection recorded.")

    def cycle(self):

        self.heartbeat()
        self.reflect()

    def _loop(self):

        while self.running:

            try:

                self.cycle()

            except Exception as e:

                print(f"[LivingCycle] Error: {e}")

            time.sleep(self.interval)

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

        print("[LivingCycle] Daemon started.")

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        print("[LivingCycle] Daemon stopped.")


if __name__ == "__main__":

    print("Living Cycle Daemon v1.1 Test Mode")

    daemon = LivingCycleDaemon(interval=10)

    daemon.start()

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        daemon.stop()
