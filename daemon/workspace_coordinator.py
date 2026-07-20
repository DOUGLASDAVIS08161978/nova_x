"""
═══════════════════════════════════════════════════════════════════════
NOVA-X WORKSPACE COORDINATOR
═══════════════════════════════════════════════════════════════════════

Coordinates communication between daemon services.

Author:
Douglas Davis & OpenAI
"""

from collections import deque
from datetime import datetime


class WorkspaceCoordinator:

    def __init__(self):

        self.queue = deque()
        self.history = []

    def submit(self, source, task_type, payload=None):

        item = {
            "timestamp": datetime.now(),
            "source": source,
            "type": task_type,
            "payload": payload or {}
        }

        self.queue.append(item)

        print(
            f"[Workspace] queued -> {task_type}"
        )

    def has_work(self):

        return len(self.queue) > 0

    def next_task(self):

        if not self.queue:
            return None

        task = self.queue.popleft()

        self.history.append(task)

        return task

    def pending(self):

        return len(self.queue)

    def processed(self):

        return len(self.history)

    def status(self):

        print("\n========== WORKSPACE ==========\n")

        print(
            "Pending :",
            self.pending()
        )

        print(
            "Processed:",
            self.processed()
        )


###############################################################
# SELF TEST
###############################################################

if __name__ == "__main__":

    ws = WorkspaceCoordinator()

    ws.submit(
        "Curiosity",
        "research_request",
        {
            "topic":"Alternating Current"
        }
    )

    ws.submit(
        "Research",
        "reflection",
        {
            "topic":"Alternating Current"
        }
    )

    ws.status()

    print()

    while ws.has_work():

        task = ws.next_task()

        print(
            "[Processing]",
            task["type"],
            task["payload"]
        )

    print()

    ws.status()

