import engine as en


class PubSubParams:
    def __init__(self):
        pass

    subscriptions = {}


def subscribe(subscriber, event):
    if event in PubSubParams.subscriptions.keys():
        PubSubParams.subscriptions[event].append(subscriber)
    else:
        PubSubParams.subscriptions[event] = [subscriber]


def publish(event, publisher, data=None):
    if event not in PubSubParams.subscriptions.keys():
        return

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
