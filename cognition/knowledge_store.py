"""
═══════════════════════════════════════════════════════════════════════
NOVA-X KNOWLEDGE STORE
═══════════════════════════════════════════════════════════════════════

Stores knowledge updates produced by the Research Engine.

Author:
Douglas Davis & OpenAI
"""

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "daemon")
)

from runtime import NovaRuntime


class KnowledgeStore:

    def __init__(self, runtime):

        self.runtime = runtime

        self.memory = []

    def cycle(self):

        if not self.runtime.workspace.has_work():

            print("[Knowledge] No work.")
            return

        task = self.runtime.workspace.next_task()

        if task["type"] != "knowledge_update":

            print(
                f"[Knowledge] Ignoring {task['type']}"
            )

            return

        self.memory.append(task["payload"])

        print()

        print("=" * 55)
        print("KNOWLEDGE STORE")
        print("=" * 55)

        print()

        print(
            f"Stored: {task['payload']['topic']}"
        )

        print(
            f"Knowledge Entries: {len(self.memory)}"
        )

        self.runtime.workspace.submit(

            "Knowledge",

            "reflection_request",

            task["payload"]

        )


###############################################################
# SELF TEST
###############################################################

if __name__ == "__main__":

    runtime = NovaRuntime()

    runtime.workspace.submit(

        "Research",

        "knowledge_update",

        {
            "topic":"Improve Battery Technology",
            "summary":"Research completed."
        }

    )

    ks = KnowledgeStore(runtime)

    ks.cycle()

    print()

    runtime.workspace.status()

