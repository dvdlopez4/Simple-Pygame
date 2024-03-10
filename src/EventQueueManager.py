
from Entity.entity import Entity
from typing import List


class EventMessage(object):
    def __init__(self, message: str, reference: Entity):
        self.message: str = message
        self.reference_entity: Entity = reference


class EventObserver(object):
    def __init__(self):
        super(EventObserver, self).__init__()

    def on_notify(self, event_message: EventMessage):
        pass


class HealthEventObserver(EventObserver):
    def __init__(self):
        super(HealthEventObserver, self).__init__()

    def on_notify(self, event_message: EventMessage):
        if (event_message.message == "Health"):
            print("Health changed!")


class EventQueueManager(object):
    events: List[EventMessage] = []
    subscribers: List[EventObserver] = []

    @staticmethod
    def add_event(message: EventMessage):
        EventQueueManager.events.append(message)
        for subscriber in EventQueueManager.subscribers:
            subscriber.on_notify(message)

    @staticmethod
    def add_subscriber(subscriber: EventObserver):
        EventQueueManager.subscribers.append(subscriber)


class EventProducer(object):
    def __init__(self):
        pass

    def produce_event(self):
        EventQueueManager.add_event(EventMessage("Health", None))


class TestGraphicsComponent(HealthEventObserver):
    def __init__(self):
        pass

    def render(self):
        pass
