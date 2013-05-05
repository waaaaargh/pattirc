import json

from appdotnet import appdotnet

from channel import Channel

class Client:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api = appdotnet.appdotnet(access_token=access_token)
        self.channels = []

    def get_my_channels(self):
        channels = json.loads(self.api.getChannels(include_annotations="1"))
        channel_objs = channels['data']
        for c in channel_objs:
            c_id = c['id']
            c_name = None
            for a in c['annotations']:
                if a['type'] == 'net.patter-app.settings':
                    c_name  = a['value']['name']
            new_channel = Channel(self, c_id, c_name)
            self.channels.append(new_channel)
