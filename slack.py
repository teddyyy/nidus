# -*- coding: utf-8 -*-

from slackclient import SlackClient

class Slack:

    def __init__(self, token):
        self.client = SlackClient(token)

    def post(self, channel, text, username):
        self.client.api_call("chat.postMessage",
                             channel=channel,
                             text=text,
                             username=username)
