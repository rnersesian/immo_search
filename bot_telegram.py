from immo_source import Estate
import requests

class BotTelegram():

    def __init__(self, username, token, chat_id):
        self.username = username
        self.token = token
        self.base_url = "https://api.telegram.org/bot" + self.token
        self.chat_id = chat_id
    
    def send_message(self):
        requests.post()

    def send_error(self):
        pass

    def send_estate(self, estate: Estate):
        pass