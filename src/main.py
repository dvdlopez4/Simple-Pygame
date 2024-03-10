#!/usr/bin/env python

from EventQueueManager import EventQueueManager
from EventQueueManager import EventProducer
from EventQueueManager import HealthEventObserver


def main():

    EventQueueManager.add_subscriber(HealthEventObserver())
    ep = EventProducer()

    print(EventQueueManager.subscribers)
    ep.produce_event()
    return 0


if __name__ == '__main__':
    main()
