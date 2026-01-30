from . import ImmoSource, Estate
import json
import requests
from typing import List

foncia_api_url = "https://fnc-api.prod.fonciatech.net/annonces/annonces/search"
foncia_base_url = "https://www.foncia.com"

request_header = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://www.foncia.com",
    "Referer": "https://www.foncia.com/",
}

request_body = {
    "type": "transaction",
    "filters": {
        "localities": {
            "slugs": [
                "lyon-69",
                "oullins-69600",
                "villeurbanne-69100",
                "la-mulatiere-69350",
            ]
        },
        "prix": {"max": 160000},
        "nbPiece": {"min": 3},
    },
    "expandNearby": True,
    "size": 15,
}


class Foncia(ImmoSource):
    def __init__(self, immo_id, base_url="https://www.foncia.com"):
        super().__init__(immo_id)
        self.base_url = base_url

    def update_data(self):
        r = requests.post(foncia_api_url, json=request_body, headers=request_header)
        if r.status_code < 200 or r.status_code >= 300:
            print(
                f"Failed to access URL :\n{foncia_api_url}\n got status code '{r.status_code}'"
            )
            return []

        data = json.loads(r.text)
        ads = data["annonces"]

        estates: List[Estate] = []
        for ad in ads:
            ad_id = str(ad["reference"])
            ad_label = ad["typeBien"]
            ad_url = self.base_url + ad["canonicalUrl"]
            price = str(ad["prixVente"])
            ad_price = f"{price[:-3]} {price[-3:]} €"
            ad_location = ad["localisation"]["locality"]["libelleDisplay"]
            ad_layout = str(ad["surface"]["habitable"]) + " m²"
            ad_layout += " - " + str(ad["nbPiece"]) + " pièces"

            estates.append(
                Estate(
                    id=ad_id,
                    label=ad_label,
                    price=ad_price,
                    layout=ad_layout,
                    location=ad_location,
                    url=ad_url,
                )
            )

        return estates
