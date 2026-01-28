import os
from dotenv import load_dotenv
from bot_telegram import BotTelegram
from immo_source import Estate
import requests


load_dotenv()
TG_USERNAME = os.getenv("TG_BOT_API_USERNAME")
TG_TOKEN = os.getenv("TG_BOT_API_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

some_estate = Estate(
    id="1",
    label="Appartement T3 à vendre",
    price="142 100 €",
    layout="3 pièces - 65,07",
    location="ST PRIEST  - 69",
    url="https://www.century21-granderue-oullins.com/trouver_logement/detail//11894785633"
)

chatbot = BotTelegram(
    username=TG_USERNAME,
    token=TG_TOKEN,
    chat_id=TG_CHAT_ID
)

requests.post(chatbot.base_url + "/sendMessage",
    data={
        "chat_id": chatbot.chat_id,
        "text": some_estate.format_to_message(),
        "parse_mode": "HTML"
    }    
)