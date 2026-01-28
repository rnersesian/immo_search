from abc import ABC, abstractmethod
from typing import List
import csv

class Estate():
    def __init__(self, label="", price="", layout="", location="", url="", id=""):
        self.label = label
        self.price = price
        self.layout = layout
        self.location = location
        self.url = url
        self.id = id

    def format_to_message(self):
        return f"""<b>Nouvelle annonce :</b>\n{self.location}\n{self.layout}\n{self.price}\n<a href="{self.url}">Lien de l'annonce</a>\n"""


    def __str__(self):
        return self.url
                

class ImmoSource(ABC):
    def __init__(self, immo_id):
        # Useful for making unique ad ids
        self.immo_id = immo_id
        # base url of the website
        self.base_url = ""
        # url for list of ads
        self.ads_list_url = ""
        # url for ad detail
        self.ad_detail_url = ""
        self.timeout_duration = 5. # value in seconds

        pass
    
    @abstractmethod
    def update_data(self) -> List[Estate]:
        pass

    def send_data(self, message=None):
        if message is not None:
            print(message)

