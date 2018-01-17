import pusherclient
import time

ZOONIVERSE_CHANNEL = "panoptes"
ZOONIVERSE_APPKEY = "79e8e05ea522377ba6db"

class PusherWrapper():
    def __init__(self):
        self.pusher = pusherclient.Pusher(ZOONIVERSE_APPKEY)
        self.pusher.connection.bind("pusher:connection_established", self.on_connect)
        self.callback = lambda data: data

    def connect(self):
        self.pusher.connect()

    def on_connect(self, data):
        channel = self.pusher.subscribe(ZOONIVERSE_CHANNEL)
        channel.bind("classification", self.on_classification)

    def on_classification(self, data):
        self.callback(data)
