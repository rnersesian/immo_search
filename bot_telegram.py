from immo_source import Estate
import requests

class BotTelegram():

    def __init__(self, username, token, chat_id):
        self.username = username
        self.token = token
        self.base_url = "https://api.telegram.org/bot" + self.token
        self.chat_id = chat_id
    

    def send_message(self, message, parse_mode="HTML"):
        requests.post(self.base_url + "/sendMessage",
            data={
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            })
        

    def post_request(self, url, data={}):
        requests.post(self.base_url + url, data=data)


    def send_error(self, error_message):
        formatted_error = f"<b>Erreur</b>\n{error_message}"
        self.send_message(formatted_error)


    def send_estate(self, estate: Estate):
        self.send_message(estate.format_to_message())