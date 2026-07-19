#!/usr/bin/env python3
"""
===========================================================
NOVA-X Event Bus v1.0
===========================================================

Internal communication layer.

Allows modules to:
- Publish events
- Subscribe to events
- Share information
- Reduce direct dependencies

Future:
- External message queues
- Distributed agents
- Async processing
===========================================================
"""

from datetime import datetime


class EventBus:

    def __init__(self):

        self.events = []

        self.subscribers = {}


    def subscribe(self, event_type, callback):

        if event_type not in self.subscribers:

            self.subscribers[event_type] = []

        self.subscribers[event_type].append(callback)


    def publish(
        self,
        event_type,
        data=None
    ):

        event = {

            "time":
                str(datetime.now()),

            "type":
                event_type,

            "data":
                data

        }

        self.events.append(event)


        print(
            f"[EventBus] Published: {event_type}"
        )


        if event_type in self.subscribers:

            for callback in self.subscribers[event_type]:

                callback(event)


        return event


    def recent(self, count=10):

        return self.events[-count:]


    def status(self):

        return {

            "events":
                len(self.events),

            "subscribers":
                len(self.subscribers)

        }


if __name__ == "__main__":


    bus = EventBus()


    def memory_listener(event):

        print(
            "[Memory Module Received]",
            event
        )


    bus.subscribe(
        "learning_event",
        memory_listener
    )


    bus.publish(

        "learning_event",

        {
            "lesson":
            "Modular systems scale better."
        }

    )


    print()

    print(
        bus.status()
    )
