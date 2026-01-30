from . import ImmoSource, Estate
from typing import List
import requests
import json

iad_api_url = "https://www.iadfrance.fr/api/properties?serpSlug=pg-lyon_69&serpSlug=vente&serpSlug=t3&location=la-mulatiere-69350&location=oullins-69600&location=villeurbanne-69100&projectType=ancien&priceMax=160000&locale=fr"

class IAD(ImmoSource):

    def __init__(self, immo_id, base_url="https://www.iadfrance.fr"):
        super().__init__(immo_id)
        self.base_url = base_url

    
    def update_data(self):
        r = requests.get(iad_api_url)
        if r.status_code < 200 and r.status_code >= 300:
            print(f"Failed to access URL :\n{self.api_url}\n got status code '{r.status_code}'")
            return
        data = json.loads(r.text)
        ads = data["items"]
        estate_list: List[Estate] = []

        for ad in ads:
            ad_id = ad["propertyListingRef"]
            ad_location = f"{ad["location"]["place"]} - {ad["location"]["postcode"]}"

            room_data = ad["rooms"]
            nb_rooms = "?"
            for room in room_data:
                if room["type"] == "rooms":
                    nb_rooms = str(room["value"])

            surface_data = ad["surfaceList"]
            ad_surface = "?? m²"
            for surface in surface_data:
                if surface["type"] == "living-area":
                    ad_surface = f"{surface["value"]} m²"
            
            ad_layout = f"{nb_rooms} pièces - {ad_surface}"
            ad_price = ad["price"]["formatted"]
            ad_label = ad["title"]
            ad_url = f"{self.base_url}/annonce/{ad["slugs"]["fr"]}/r{ad["propertyListingRef"]}"

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
        