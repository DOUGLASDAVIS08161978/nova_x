"""
═══════════════════════════════════════════════════════════════════════
NOVA-X RUNTIME
═══════════════════════════════════════════════════════════════════════

Central runtime object.

Author:
Douglas Davis & OpenAI
"""

from config import ConfigManager
from event_bus import EventBus
from scheduler import Scheduler
from heartbeat import Heartbeat
from mission_manager import MissionManager
from plugin_loader import PluginLoader
from workspace_coordinator import WorkspaceCoordinator
from service_manager import ServiceManager
from task_registry import TaskRegistry


class NovaRuntime:

    def __init__(self):

        print("[Runtime] Initializing...")

        self.config = ConfigManager()
        self.config.load()

        self.event_bus = EventBus()

        self.scheduler = Scheduler()

        self.heartbeat = Heartbeat()

        self.workspace = WorkspaceCoordinator()

        self.missions = MissionManager()

        self.plugins = PluginLoader()

        self.services = ServiceManager()

        self.registry = TaskRegistry()

        print("[Runtime] Ready.")

    def summary(self):

        print("\n========== NOVA-X RUNTIME ==========\n")

        print("Config          ✓")
        print("Event Bus       ✓")
        print("Scheduler       ✓")
        print("Heartbeat       ✓")
        print("Workspace       ✓")
        print("Mission Manager ✓")
        print("Plugin Loader   ✓")
        print("Service Manager ✓")
        print("Task Registry   ✓")

        print()


##############################################################
# SELF TEST
##############################################################

if __name__ == "__main__":

    runtime = NovaRuntime()

    runtime.summary()
