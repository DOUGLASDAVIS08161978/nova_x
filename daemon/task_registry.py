"""
═══════════════════════════════════════════════════════════════════════
NOVA-X TASK REGISTRY
═══════════════════════════════════════════════════════════════════════

Registers recurring daemon tasks.

Author:
Douglas Davis & OpenAI
"""

import time


class RegisteredTask:

    def __init__(self, name, interval, callback):

        self.name = name
        self.interval = interval
        self.callback = callback
        self.last_run = 0
        self.run_count = 0

    def due(self):

        return (time.time() - self.last_run) >= self.interval

    def execute(self):

        self.last_run = time.time()
        self.run_count += 1

        print(f"[Task] {self.name}")

        try:
            self.callback()

        except Exception as e:

            print(f"[Task Error] {e}")


class TaskRegistry:

    def __init__(self):

        self.tasks = []

    def register(self, name, interval, callback):

        task = RegisteredTask(
            name,
            interval,
            callback
        )

        self.tasks.append(task)

        print(
            f"[Registry] Registered {name}"
        )

    def tick(self):

        for task in self.tasks:

            if task.due():

                task.execute()

    def status(self):

        print("\n========== TASKS ==========\n")

        if not self.tasks:

            print("No registered tasks.\n")
            return

        for task in self.tasks:

            print(
                f"{task.name:<25}"
                f"Runs: {task.run_count}"
            )


###############################################################
# SELF TEST
###############################################################

if __name__ == "__main__":

    registry = TaskRegistry()

    def curiosity():

        print("Curiosity cycle...")

    def reflection():

        print("Reflection cycle...")

    registry.register(
        "Curiosity",
        2,
        curiosity
    )

    registry.register(
        "Reflection",
        5,
        reflection
    )

    print("\nRunning registry...\n")

    start = time.time()

    while time.time() - start < 12:

        registry.tick()

        time.sleep(1)

    registry.status()

