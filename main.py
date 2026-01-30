import os
from dotenv import load_dotenv

from immo_source.century21 import Century21
from immo_source.laforet import Laforet
from immo_source.orpi import Orpi
from immo_source.guyhoquet import GuyHoquet
from immo_source.era_immobilier import EraImmobilier
from immo_source.iad import IAD
from immo_source.safti import Safti
from immo_source.foncia import Foncia

from bot_telegram import BotTelegram
from immo_searcher import ImmoSearcher


if __name__ == "__main__":
    load_dotenv()
    TG_BOT_USERNAME = os.getenv("TG_BOT_API_USERNAME")
    TG_BOT_TOKEN = os.getenv("TG_BOT_API_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")

    IS = ImmoSearcher(
        sources=[
            Orpi(immo_id="ORPI", base_url="https://www.orpi.com"),
            Century21(
                immo_id="C21_GR_Oullins",
                base_url="https://www.century21-granderue-oullins.com",
            ),
            Century21(
                immo_id="C21_VB_Zola",
                base_url="https://www.century21-vu-villeurbanne-zola.com",
            ),
            Century21(
                immo_id="C21_LDI_Lyon8",
                base_url="https://www.century21-hestia-ldi-lyon-8.com",
            ),
            Century21(
                immo_id="C21_Dauph_Lacass",
                base_url="https://www.century21-dauphine-lacassagne-lyon.com",
            ),
            Century21(
                immo_id="C21_Rive_Gauche",
                base_url="https://www.century21-rg-lyon-6.com",
            ),
            Century21(
                immo_id="C21_Presquile",
                base_url="https://www.century21-pi-immobilier-69000.com",
            ),
            Century21(
                immo_id="C21_Lyon4",
                base_url="https://www.century21-perspective-lyon-4.com",
            ),
            Century21(
                immo_id="C21_Tassin", base_url="https://www.century21-ldl-tassin.com"
            ),
            Century21(
                immo_id="C21_VB_Decker",
                base_url="https://www.century21-vu-villeurbanne-becker.com",
            ),
            Laforet(
                immo_id="LF_Oullins",
                base_url="https://www.laforet.com/agence-immobiliere/oullins",
            ),
            Laforet(
                immo_id="LF_Lyon2",
                base_url="https://www.laforet.com/agence-immobiliere/lyon2",
            ),
            Laforet(
                immo_id="LF_Lyon3_MCHT",
                base_url="https://www.laforet.com/agence-immobiliere/lyon3-montchat",
            ),
            Laforet(
                immo_id="LF_Lyon3_PD",
                base_url="https://www.laforet.com/agence-immobiliere/lyon3-partdieu",
            ),
            Laforet(
                immo_id="LF_Lyon4",
                base_url="https://www.laforet.com/agence-immobiliere/lyon4",
            ),
            Laforet(
                immo_id="LF_Lyon7",
                base_url="https://www.laforet.com/agence-immobiliere/lyon-7",
            ),
            Laforet(
                immo_id="LF_Lyon8",
                base_url="https://www.laforet.com/agence-immobiliere/lyon8",
            ),
            Laforet(
                immo_id="LF_VB_Rep",
                base_url="https://www.laforet.com/agence-immobiliere/villeurbanne-republique",
            ),
            GuyHoquet(immo_id="GH_Oullins", base_url="https://oullins.guy-hoquet.com"),
            GuyHoquet(
                immo_id="GH_Lyon3", base_url="https://lyon-3-montchat.guy-hoquet.com"
            ),
            GuyHoquet(immo_id="GH_Lyon4", base_url="https://lyon-4.guy-hoquet.com/"),
            GuyHoquet(
                immo_id="GH_Lyon6", base_url="https://lyon-6-rhone.guy-hoquet.com"
            ),
            GuyHoquet(immo_id="GH_Lyon7", base_url="https://lyon-7-sud.guy-hoquet.com"),
            GuyHoquet(immo_id="GH_Lyon9", base_url="https://lyon-9.guy-hoquet.com/"),
            GuyHoquet(
                immo_id="GH_Bron", base_url="https://villeurbanne-zola.guy-hoquet.com"
            ),
            GuyHoquet(
                immo_id="GH_VB", base_url="https://villeurbanne-zola.guy-hoquet.com"
            ),
            EraImmobilier(immo_id="ERA_Lyon2", agency_id="316"),
            EraImmobilier(immo_id="ERA_Lyon3", agency_id="262"),
            EraImmobilier(immo_id="ERA_Lyon7", agency_id="245"),
            EraImmobilier(immo_id="ERA_VB_GC", agency_id="195"),
            IAD(immo_id="IAD"),
            Safti(immo_id="SAFTI"),
            Foncia(immo_id="FNCIA"),
        ],
        chatbot=BotTelegram(
            username=TG_BOT_USERNAME, token=TG_BOT_TOKEN, chat_id=TG_CHAT_ID
        ),
    )

    IS.run()
