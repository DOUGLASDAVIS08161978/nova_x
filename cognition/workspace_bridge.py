#!/usr/bin/env python3
"""
===========================================================
NOVA-X Workspace Bridge v1.1
===========================================================

Connects perception modules to the Global Workspace
using structured events.

Features
--------
- Structured event publishing
- Metadata preservation
- Visual observation category
- Future-ready for additional sensors

===========================================================
"""

from datetime import datetime

from core.global_workspace import GlobalWorkspace


class WorkspaceBridge:

    def __init__(self, workspace=None):

        self.workspace = workspace or GlobalWorkspace()

        self.forwarded = 0


    def publish_observation(self, observation):

        event = {

            "type": observation.get(
                "type",
                "visual_observation"
            ),

            "image": observation.get(
                "image"
            ),

            "status": observation.get(
                "status",
                "captured"
            ),

            "confidence": observation.get(
                "confidence",
                1.0
            ),

            "timestamp": observation.get(
                "timestamp",
                str(datetime.now())
            )

        }


        message = (
            f"Visual observation received: "
            f"{event['image']}"
        )


        try:

            self.workspace.broadcast(

                source="ObservationEngine",

                message=message,

                category="visual_observation",

                metadata=event

            )

        except TypeError:

            # Compatibility with older GlobalWorkspace versions

            self.workspace.broadcast(

                "ObservationEngine",

                message

            )


        self.forwarded += 1

        return event


    def status(self):

        return {

            "forwarded_observations":
                self.forwarded

        }


if __name__ == "__main__":

    workspace = GlobalWorkspace()

    bridge = WorkspaceBridge(
        workspace
    )

    observation = {

        "type":
            "visual_observation",

        "image":
            "images/test.jpg",

        "status":
            "captured",

        "confidence":
            1.0,

        "timestamp":
            str(datetime.now())

    }

    print()

    print("NOVA-X Workspace Bridge v1.1")

    print("============================")

    result = bridge.publish_observation(
        observation
    )

    print()

    print(result)

    print()

    print("Status")

    print("------")

    print(
        bridge.status()
    )

    print()

    print("Workspace Events")

    print("----------------")

    if hasattr(workspace, "get_events"):

        for event in workspace.get_events():

            print(event)
