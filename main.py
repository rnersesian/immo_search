# import requests
# from bs4 import BeautifulSoup
# from typing import List
# from immo_source.century21 import Century21
# from immo_source.laforet import Laforet
# from immo_source.orpi import Orpi
# from immo_source import ImmoSource

# laforet_oullins = Laforet(immo_id="Laforet_Oullins", base_url="https://www.laforet.com/agence-immobiliere/oullins")
# laforet_oullins.update_data()

# immo_sources: List[ImmoSource] = [
#     Laforet(immo_id="LF_Oullins", base_url="https://www.laforet.com/agence-immobiliere/oullins"),
#     Century21(immo_id="C21_GR_Oullins", base_url="https://www.century21-granderue-oullins.com"),
#     Century21(immo_id="C21_VB_Zola", base_url="https://www.century21-vu-villeurbanne-zola.com"),
#     Orpi(immo_id="ORPI", base_url="https://www.orpi.com")
# ]

# for source in immo_sources:
#     source.update_data()

import os
from dotenv import load_dotenv
from immo_searcher import ImmoSearcher
from immo_source.century21 import Century21
from immo_source.laforet import Laforet
from immo_source.orpi import Orpi
from bot_telegram import BotTelegram


if __name__ == "__main__":

    load_dotenv()
    TG_BOT_USERNAME = os.getenv("TG_BOT_API_USERNAME")
    TG_BOT_TOKEN = os.getenv("TG_BOT_API_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")

    IS = ImmoSearcher(
        sources=[
            Laforet(immo_id="LF_Oullins", base_url="https://www.laforet.com/agence-immobiliere/oullins"),
            Century21(immo_id="C21_GR_Oullins", base_url="https://www.century21-granderue-oullins.com"),
            Century21(immo_id="C21_VB_Zola", base_url="https://www.century21-vu-villeurbanne-zola.com"),
            Orpi(immo_id="ORPI", base_url="https://www.orpi.com")
        ],
        chatbot=BotTelegram(
            username=TG_BOT_USERNAME,
            token=TG_BOT_TOKEN,
            chat_id=TG_CHAT_ID
        )
    )

    IS.run()