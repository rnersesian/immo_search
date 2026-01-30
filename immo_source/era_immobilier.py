from . import ImmoSource, Estate
from typing import List
import requests
import json

# https://api.eraimmobilier.com/api/v2/annonces/search?page=1&type_annonce=vente&nb_pieces=3&prix_to=440000&per_page=8&order_dir=desc&statut=0,1,11&agence_id=262

era_api_url = "https://api.eraimmobilier.com/api/v2/annonces/search?page=1&type_annonce=vente&nb_pieces=3&prix_to=160000&per_page=8&order_dir=desc&statut=0,1,11&agence_id="

class EraImmobilier(ImmoSource):

    def __init__(self, immo_id, agency_id, base_url="https://www.eraimmobilier.com"):
        super().__init__(immo_id)
        self.base_url = base_url
        self.api_url = era_api_url + str(agency_id)
        self.agency_id = agency_id
        

    def update_data(self):
        r = requests.get(self.api_url)
        if r.status_code < 200 and r.status_code >= 300:
            print(f"Failed to access URL :\n{self.api_url}\n got status code '{r.status_code}'")
            return
        data = json.loads(r.text)
        ads = data["data"]

        estate_list: List[Estate] = []

        for ad in ads:
            ad_id = ad["id"]
            ad_label = ad["type_bien"]
            ad_price = ad["prix"]
            ad_layout = f"{ad["surface_habitable"]} m² - {ad["nb_pieces"]} pièces"
            ad_location = f"{ad["code_postal"]} - {ad["ville"]}"
            ad_url = f"{self.base_url}/{ad["agence"]["slug"]}/annonces/{ad_id}"

            estate_list.append(
                Estate(
                    id=ad_id,
                    label=ad_label,
                    price=ad_price,
                    layout=ad_layout,
                    location=ad_location,
                    url=ad_url
            ))
        return estate_list

