"""
═══════════════════════════════════════════════════════════════
NOVA-X MISSION MANAGER
═══════════════════════════════════════════════════════════════

Tracks long-term research missions.

Author:
Douglas Davis & OpenAI
"""

from datetime import datetime


class Mission:

    def __init__(self, name, priority="NORMAL"):

        self.name = name
        self.priority = priority
        self.progress = 0
        self.questions_remaining = 0
        self.completed = False
        self.created = datetime.now()

    def advance(self, amount=5):

        if self.completed:
            return

        self.progress += amount

        if self.progress >= 100:
            self.progress = 100
            self.completed = True

    def add_questions(self, count):

        self.questions_remaining += count

    def answer_question(self):

        if self.questions_remaining > 0:
            self.questions_remaining -= 1

    def status(self):

        state = "COMPLETE" if self.completed else "ACTIVE"

        return {
            "Mission": self.name,
            "Priority": self.priority,
            "Progress": f"{self.progress}%",
            "Questions": self.questions_remaining,
            "State": state
        }


class MissionManager:

    def __init__(self):

        self.missions = []

    def add(self, mission):

        self.missions.append(mission)

        print(f"[Mission] Added: {mission.name}")

    def list(self):

        print("\n========== MISSIONS ==========\n")

        if not self.missions:
            print("No active missions.\n")
            return

        for mission in self.missions:

            s = mission.status()

            print(f"Mission   : {s['Mission']}")
            print(f"Priority  : {s['Priority']}")
            print(f"Progress  : {s['Progress']}")
            print(f"Questions : {s['Questions']}")
            print(f"State     : {s['State']}")
            print()

    def active(self):

        return [
            m for m in self.missions
            if not m.completed
        ]

    def next_mission(self):

        active = self.active()

        if not active:
            return None

        active.sort(
            key=lambda m: (
                m.priority != "HIGH",
                m.progress
            )
        )

        return active[0]


###############################################################
# Self Test
###############################################################

if __name__ == "__main__":

    manager = MissionManager()

    battery = Mission(
        "Improve Battery Technology",
        "HIGH"
    )

    battery.add_questions(12)
    battery.advance(25)

    ai = Mission(
        "Expand AI Knowledge",
        "NORMAL"
    )

    ai.add_questions(7)
    ai.advance(10)

    manager.add(battery)
    manager.add(ai)

    manager.list()

    next_job = manager.next_mission()

    print("Next Mission:\n")

    print(next_job.name)

