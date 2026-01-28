import requests
from bs4 import BeautifulSoup
from typing import List
from immo_source.century21 import Century21
from immo_source.laforet import Laforet
from immo_source.orpi import Orpi
from immo_source import ImmoSource

laforet_oullins = Laforet(immo_id="Laforet_Oullins", base_url="https://www.laforet.com/agence-immobiliere/oullins")
laforet_oullins.update_data()

immo_sources: List[ImmoSource] = [
    Laforet(immo_id="LF_Oullins", base_url="https://www.laforet.com/agence-immobiliere/oullins"),
    Century21(immo_id="C21_GR_Oullins", base_url="https://www.century21-granderue-oullins.com"),
    Century21(immo_id="C21_VB_Zola", base_url="https://www.century21-vu-villeurbanne-zola.com"),
    Orpi(immo_id="ORPI", base_url="https://www.orpi.com")
]

for source in immo_sources:
    source.update_data()