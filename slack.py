import requests

url = 'https://slack.com/api/chat.postMessage'

class Slack:

    def __init__(self, token):
        self.token = token

    def post(self, channel, text):
        data = {
            'token': self.token, # Bot User OAuth Token
            'channel': channel,
            'text': text
        }

        response = requests.post(url, data=data)
        print(response.text)
