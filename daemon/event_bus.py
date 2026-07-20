"""
═══════════════════════════════════════════════════════════════
NOVA-X EVENT BUS
═══════════════════════════════════════════════════════════════

Publish / Subscribe Event System

Author:
Douglas Davis & OpenAI
"""

from collections import defaultdict
from datetime import datetime
import traceback


class Event:

    def __init__(self, name, data=None):

        self.name = name
        self.data = data or {}
        self.timestamp = datetime.now()

    def __str__(self):

        return f"<Event {self.name}>"


class EventBus:

    def __init__(self):

        self.listeners = defaultdict(list)
        self.history = []

    def subscribe(self, event_name, callback):

        self.listeners[event_name].append(callback)

        print(f"[EventBus] subscribed -> {event_name}")

    def unsubscribe(self, event_name, callback):

        if callback in self.listeners[event_name]:
            self.listeners[event_name].remove(callback)

    def publish(self, event_name, **kwargs):

        event = Event(event_name, kwargs)

        self.history.append(event)

        print(f"[EventBus] {event_name}")

        for callback in list(self.listeners[event_name]):

            try:

                callback(event)

            except Exception:

                traceback.print_exc()

    def listener_count(self):

        return sum(
            len(v)
            for v in self.listeners.values()
        )

    def event_count(self):

        return len(self.history)

    def clear_history(self):

        self.history.clear()

    def dump_history(self):

        print("\nEVENT HISTORY\n")

        for event in self.history:

            print(
                event.timestamp.strftime("%H:%M:%S"),
                event.name,
                event.data
            )


bus = EventBus()


###############################################################
# Self Test
###############################################################

if __name__ == "__main__":

    print("\n===== EVENT BUS TEST =====\n")

    def curiosity(event):

        print(
            "[Curiosity]",
            event.data
        )

    def journal(event):

        print(
            "[Journal]",
            event.name
        )

    bus.subscribe(
        "research_completed",
        curiosity
    )

    bus.subscribe(
        "research_completed",
        journal
    )

    bus.publish(
        "research_completed",
        topic="Alternating Current",
        source="DuckDuckGo"
    )

    print()

    print(
        "Listeners:",
        bus.listener_count()
    )

    print(
        "Events:",
        bus.event_count()
    )

    print()

    bus.dump_history()
