from . import ImmoSource, Estate
import json
import requests
from typing import List

safti_api_url = "https://api.safti.fr/public_site/property/search"

request_header = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://www.safti.fr",
    "Referer": "https://www.safti.fr/"
}

request_body = {
    "transactionType":"vente",
    "propertyType":["appartement", "maison"],
    "locations":["city_all_cp-30526","city-30545","city-30552","city-30672"],
    "page":1,
    "budgetMax":160000,
    "roomNumber":"3",
    "limit":24
}

class Safti(ImmoSource):

    def __init__(self, immo_id, base_url="https://www.safti.fr/annonces/achat/appartement"):
        super().__init__(immo_id)
        self.base_url = base_url

    def update_data(self):
        r = requests.post(safti_api_url, json=request_body, headers=request_header)
        if r.status_code < 200 and r.status_code >= 300:
            print(f"Failed to access URL :\n{self.api_url}\n got status code '{r.status_code}'")
            return
        data = json.loads(r.text)
        ads = data["properties"]

        estates: List[Estate] = []
        for ad in ads:
            ad_url = f"{self.base_url}/{ad["city"].lower().replace(" ", "-")}-{ad["postCode"]}/{ad["propertyReference"]}"
            price = str(ad["price"])
            ad_price = f"{price[:-3]} {price[-3:]} €"
            ad_location = ad["city"]
            ad_layout = f"{ad["roomNumber"]} pièces - {ad["propertySurface"]} m²"
            ad_label = ad["propertyType"]
            ad_id = str(ad["propertyReference"])

            estates.append(Estate(
                id=ad_id,
                label=ad_label,
                price=ad_price,
                layout=ad_layout,
                location=ad_location,
                url=ad_url
            ))

        return estates