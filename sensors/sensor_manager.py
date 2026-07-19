#!/usr/bin/env python3
"""
===========================================================
NOVA-X Sensor Manager v1.0
===========================================================

Foundation layer for device perception.

Responsibilities:
- Register sensor modules
- Track available capabilities
- Publish sensor events
- Keep hardware access modular

This module does not access hardware directly.
Individual sensor plugins handle that.

===========================================================
"""

from datetime import datetime


class SensorManager:

    def __init__(self):

        self.sensors = {}

        self.events = []


    def register_sensor(self, name, description):

        self.sensors[name] = {

            "name": name,

            "description": description,

            "enabled": False

        }


        print(
            f"[SensorManager] Registered: {name}"
        )


    def enable_sensor(self, name):

        if name in self.sensors:

            self.sensors[name]["enabled"] = True

            print(
                f"[SensorManager] Enabled: {name}"
            )

            return True

        return False


    def disable_sensor(self, name):

        if name in self.sensors:

            self.sensors[name]["enabled"] = False

            return True

        return False


    def publish_event(self, source, data):

        event = {

            "time": str(datetime.now()),

            "source": source,

            "data": data

        }


        self.events.append(event)

        print(
            f"[Sensor Event] {source}: {data}"
        )


    def status(self):

        return {

            "available_sensors":
                list(self.sensors.keys()),

            "events":
                len(self.events)

        }


if __name__ == "__main__":

    manager = SensorManager()


    manager.register_sensor(

        "camera",

        "Visual input device"

    )


    manager.register_sensor(

        "microphone",

        "Audio input device"

    )


    manager.enable_sensor(

        "camera"

    )


    manager.publish_event(

        "camera",

        "Test visual observation"

    )


    print()

    print("Sensor Status")

    print("-------------")

    print(

        manager.status()

    )
