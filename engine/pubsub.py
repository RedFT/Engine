import engine as en


class PubSub(object):
    _subscriptions = {}

    @staticmethod
    def subsribe(subscriber, event):
        if event in PubSub._subscriptions.keys():
            PubSub._subscriptions[event].append(subscriber)
        else:
            PubSub._subscriptions[event] = [subscriber]

    @staticmethod
    def publish(event, publisher, data=None):
        en.GraphicalLogger.log(
            "Got event: " + str(event) + " from publisher: " + str(publisher))

        if event not in PubSub._subscriptions.keys():
            return
        for sub in PubSub._subscriptions[event]:
            notify = getattr(sub, "notify", None)
            if notify is None:
                en.GraphicalLogger.log(
                    str(sub) + " has no member called notify.")
                return

            if not callable(notify):
                en.GraphicalLogger.log(
                    str(sub) + "'s member,notify, is not callable.")
                return

            notify(event, publisher, data)

