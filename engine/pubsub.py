class PubSubParams:
    def __init__(self):
        pass

    subscriptions = {}
    message_queue = []


def subscribe(subscriber, message):
    if message in PubSubParams.subscriptions.keys():
        if subscriber in PubSubParams.subscriptions[message]:
            return
        PubSubParams.subscriptions[message].append(subscriber)
    else:
        PubSubParams.subscriptions[message] = [subscriber]

def unsubscribe_to_all_messages(subscriber):
    for message in PubSubParams.subscriptions.keys():
        if subscriber not in PubSubParams.subscriptions[message]:
            return

        PubSubParams.subscriptions[message].remove(subscriber)

def unsubscribe(subscriber, message):
    if message not in PubSubParams.subscriptions.keys():
        return

    if subscriber not in PubSubParams.subscriptions[message]:
        return

    PubSubParams.subscriptions[message].remove(subscriber)



def publish(message, publisher, *data):
    # don't put in queue if nobody is subscribe to it
    if message not in PubSubParams.subscriptions.keys():
        return

    PubSubParams.message_queue.append((message, publisher, data))


def handle_messages(dt=0):
    # notify all subscribers
    for message, publisher, data in PubSubParams.message_queue:
        for sub in PubSubParams.subscriptions[message]:
            notify = getattr(sub, "notify", None)
            if notify is None:
                return
            sub.notify(message, publisher, *data)

    # clear message queue
    PubSubParams.message_queue = []
