"""
═══════════════════════════════════════════════════════════════════════
NOVA-X MAIN DAEMON
═══════════════════════════════════════════════════════════════════════
Bootstraps the NOVA-X runtime.

Author:
Douglas Davis & OpenAI
"""

import time

from config import ConfigManager
from event_bus import EventBus
from scheduler import Scheduler
from service_manager import ServiceManager, Service
from heartbeat import Heartbeat
from mission_manager import MissionManager
from plugin_loader import PluginLoader
from workspace_coordinator import WorkspaceCoordinator


def main():

    print("\n========================================")
    print("        NOVA-X DAEMON STARTING")
    print("========================================\n")

    # Core systems
    config = ConfigManager()
    config.load()

    bus = EventBus()
    scheduler = Scheduler()
    heartbeat = Heartbeat()
    missions = MissionManager()
    workspace = WorkspaceCoordinator()
    plugins = PluginLoader()

    # Services
    services = ServiceManager()

    for name in (
        "Curiosity",
        "Research",
        "Reflection",
        "Knowledge",
        "Journal"
    ):
        services.register(Service(name))

    services.start_all()

    print()
    plugins.discover()
    print()

    print("Daemon online. Press Ctrl+C to stop.\n")

    try:

        while True:

            scheduler.tick()

            if workspace.has_work():

                task = workspace.next_task()

                print(
                    f"[Daemon] Processing {task['type']} "
                    f"from {task['source']}"
                )

            heartbeat.tick()

            time.sleep(1)

    except KeyboardInterrupt:

        print("\nStopping NOVA-X...\n")

        services.stop_all()

        print("\nFinal Heartbeat:")

        heartbeat.report()

        print("Shutdown complete.")


if __name__ == "__main__":
    main()
