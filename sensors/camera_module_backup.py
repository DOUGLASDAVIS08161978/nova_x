#!/usr/bin/env python3
"""
===========================================================
NOVA-X Camera Module v1.0
===========================================================

Connects NOVA-X to Android camera through Termux:API.

Features:
- Capture images
- Store images locally
- Publish sensor events
- Modular hardware interface

===========================================================
"""

import subprocess
from pathlib import Path
from datetime import datetime

from sensors.sensor_manager import SensorManager


class CameraModule:

    def __init__(self, sensor_manager=None):

        self.sensor_manager = sensor_manager or SensorManager()

        self.image_dir = Path(
            "images"
        )

        self.image_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def capture(self, camera_id=0):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            self.image_dir /
            f"capture_{timestamp}.jpg"
        )


        try:

            subprocess.run(

                [
                    "termux-camera-photo",
                    "-c",
                    str(camera_id),
                    str(filename)
                ],

                check=True

            )


            event = {

                "type": "image_capture",

                "camera": camera_id,

                "file": str(filename),

                "time": str(datetime.now())

            }


            self.sensor_manager.publish_event(

                "camera",

                event

            )


            return event


        except Exception as e:

            return {

                "success": False,

                "error": str(e)

            }


if __name__ == "__main__":


    manager = SensorManager()


    camera = CameraModule(

        manager

    )


    print()

    print(
        "NOVA-X Camera Test"
    )

    print(
        "=================="
    )


    result = camera.capture(

        camera_id=0

    )


    print()

    print(result)

    print()

    print(
        manager.status()
    )
