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
        return f"""<b>Nouvelle annonce : {self.label}</b>\n{self.location}\n{self.layout}\n{self.price}\n<a href="{self.url}">Lien de l'annonce</a>\n"""

    def save(self):
        with open("estates.csv", "r") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                if row["id"] == self.id:
                    return
        with open("estates.csv", "a", newline='') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([self.id, self.label, self.price, self.layout, self.location, self.url])
                

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

        pass
    
    @abstractmethod
    def update_data(self) -> List[Estate]:
        pass

    def send_data(self, message=None):
        if message is not None:
            print(message)

