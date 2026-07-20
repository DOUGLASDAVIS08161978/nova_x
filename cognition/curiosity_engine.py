"""
═══════════════════════════════════════════════════════════════════════
NOVA-X CURIOSITY ENGINE
═══════════════════════════════════════════════════════════════════════

Generates research tasks from active missions.

Author:
Douglas Davis & OpenAI
"""

class CuriosityEngine:

    def __init__(self, runtime):

        self.runtime = runtime

    def cycle(self):

        mission = self.runtime.missions.next_mission()

        if mission is None:

            print("[Curiosity] No active missions.")
            return

        task = {
            "mission": mission.name,
            "priority": mission.priority
        }

        self.runtime.workspace.submit(
            "Curiosity",
            "research_request",
            task
        )

        print(
            f"[Curiosity] Proposed research for '{mission.name}'"
        )


###############################################################
# SELF TEST
###############################################################

if __name__ == "__main__":

    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "daemon"))

    from runtime import NovaRuntime
    from mission_manager import Mission

    runtime = NovaRuntime()

    runtime.missions.add(
        Mission("Improve Battery Technology", "HIGH")
    )

    engine = CuriosityEngine(runtime)

    engine.cycle()

    runtime.workspace.status()

