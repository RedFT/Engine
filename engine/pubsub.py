import engine as en


class PubSubParams:
    def __init__(self):
        pass

    subscriptions = {}
    message_queue = []


def subscribe(subscriber, event):
    if event in PubSubParams.subscriptions.keys():
        PubSubParams.subscriptions[event].append(subscriber)
    else:
        PubSubParams.subscriptions[event] = [subscriber]


def publish(event, publisher, data=None):
    # don't put in queue if nobody is subscribe to it
    if event not in PubSubParams.subscriptions.keys():
        return

    PubSubParams.message_queue.append((event, publisher, data))


def update(dt):
    # notify all subscribers
    for event, publisher, data in PubSubParams.message_queue:
        for sub in PubSubParams.subscriptions[event]:
            notify = getattr(sub, "notify", None)
            if notify is None:
                en.graphical_logger.log(
                    str(sub) + " has no member called notify.")
                return

            if not callable(notify):
                en.graphical_logger.log(
                    str(sub) + "'s member, notify, is not callable.")
                return

            notify(event, publisher, data)

    # clear event queue
    PubSubParams.message_queue = []
