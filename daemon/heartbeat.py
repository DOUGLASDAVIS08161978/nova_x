"""
═══════════════════════════════════════════════════════════════════════
NOVA-X HEARTBEAT MONITOR
═══════════════════════════════════════════════════════════════════════

Tracks daemon runtime statistics.

Author:
Douglas Davis & OpenAI
"""

import time
from datetime import datetime


class Heartbeat:

    def __init__(self):

        self.start_time = time.time()
        self.cycles = 0
        self.events = 0
        self.research_cycles = 0
        self.reflection_cycles = 0

    def tick(self):

        self.cycles += 1

    def event(self):

        self.events += 1

    def research(self):

        self.research_cycles += 1

    def reflection(self):

        self.reflection_cycles += 1

    def uptime(self):

        return int(time.time() - self.start_time)

    def report(self):

        print("\n========== NOVA-X HEARTBEAT ==========\n")

        print(
            "Time:",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        print(
            "Uptime:",
            f"{self.uptime()} seconds"
        )

        print(
            "Daemon Cycles:",
            self.cycles
        )

        print(
            "Events:",
            self.events
        )

        print(
            "Research Cycles:",
            self.research_cycles
        )

        print(
            "Reflection Cycles:",
            self.reflection_cycles
        )

        print("\nStatus: HEALTHY\n")


##############################################################
# Self Test
##############################################################

if __name__ == "__main__":

    hb = Heartbeat()

    print("Starting heartbeat demo...\n")

    for i in range(5):

        time.sleep(1)

        hb.tick()
        hb.event()

        if i % 2 == 0:
            hb.research()

        if i % 3 == 0:
            hb.reflection()

        hb.report()
