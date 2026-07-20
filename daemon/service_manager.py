"""
═══════════════════════════════════════════════════════════════════════
NOVA-X SERVICE MANAGER
═══════════════════════════════════════════════════════════════════════

Registers and supervises daemon services.

Author:
Douglas Davis & OpenAI
"""

from datetime import datetime


class Service:

    def __init__(self, name):

        self.name = name
        self.running = False
        self.started = None

    def start(self):

        if self.running:
            return

        self.running = True
        self.started = datetime.now()

        print(f"[Service] {self.name} started")

    def stop(self):

        if not self.running:
            return

        self.running = False

        print(f"[Service] {self.name} stopped")

    def heartbeat(self):

        if self.running:
            print(f"[{self.name}] heartbeat")


class ServiceManager:

    def __init__(self):

        self.services = {}

    def register(self, service):

        self.services[service.name] = service

        print(f"[Manager] Registered {service.name}")

    def start_all(self):

        print("\nStarting Services...\n")

        for service in self.services.values():
            service.start()

    def stop_all(self):

        print("\nStopping Services...\n")

        for service in self.services.values():
            service.stop()

    def heartbeat(self):

        for service in self.services.values():
            service.heartbeat()

    def status(self):

        print("\n========== SERVICE STATUS ==========\n")

        for service in self.services.values():

            state = "RUNNING" if service.running else "STOPPED"

            print(
                f"{service.name:<20} {state}"
            )


##############################################################
# Self Test
##############################################################

if __name__ == "__main__":

    manager = ServiceManager()

    manager.register(Service("Curiosity"))
    manager.register(Service("Research"))
    manager.register(Service("Reflection"))
    manager.register(Service("Knowledge"))
    manager.register(Service("Journal"))

    manager.start_all()

    print()

    manager.heartbeat()

    manager.status()

    manager.stop_all()

    manager.status()

