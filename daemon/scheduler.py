"""
═══════════════════════════════════════════════════════════════
NOVA-X TASK SCHEDULER
═══════════════════════════════════════════════════════════════

Simple recurring task scheduler.

Author:
Douglas Davis & OpenAI
"""

import time
from datetime import datetime


class ScheduledTask:

    def __init__(self, name, interval, callback):

        self.name = name
        self.interval = interval
        self.callback = callback
        self.last_run = 0
        self.run_count = 0

    def ready(self):

        return (time.time() - self.last_run) >= self.interval

    def run(self):

        self.last_run = time.time()
        self.run_count += 1

        print(
            f"[Scheduler] Running {self.name}"
        )

        self.callback()


class Scheduler:

    def __init__(self):

        self.tasks = []

    def add_task(self, name, interval, callback):

        task = ScheduledTask(
            name,
            interval,
            callback
        )

        self.tasks.append(task)

        print(
            f"[Scheduler] Added task: {name}"
        )

    def tick(self):

        for task in self.tasks:

            if task.ready():

                task.run()

    def task_count(self):

        return len(self.tasks)

    def list_tasks(self):

        print("\nRegistered Tasks\n")

        for task in self.tasks:

            print(
                f"{task.name}"
                f"  interval={task.interval}s"
                f"  runs={task.run_count}"
            )


#########################################################
# Self Test
#########################################################

if __name__ == "__main__":

    scheduler = Scheduler()

    def curiosity():

        print(
            datetime.now().strftime("%H:%M:%S"),
            "Curiosity cycle"
        )

    def reflection():

        print(
            datetime.now().strftime("%H:%M:%S"),
            "Reflection cycle"
        )

    scheduler.add_task(
        "Curiosity",
        3,
        curiosity
    )

    scheduler.add_task(
        "Reflection",
        5,
        reflection
    )

    print("\nRunning scheduler...\n")

    start = time.time()

    while time.time() - start < 15:

        scheduler.tick()

        time.sleep(1)

    print()

    scheduler.list_tasks()
