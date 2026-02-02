from . import ImmoSource, Estate
import requests
from bs4 import BeautifulSoup
from typing import List

class Laforet(ImmoSource):
    
    def __init__(self, immo_id, base_url):
        super().__init__(immo_id)
        self.ads_list_url = f"{base_url}/acheter?filter[max]=160000&filter[rooms]=3"

    def update_data(self) -> List[Estate]:
        r = requests.get(self.ads_list_url, timeout=self.timeout_duration)
        soup = BeautifulSoup(r.text, 'html.parser')
        favorites = soup.select("div#favoriz--page--1 article")
        standards = soup.select("div#standard--page--1 article")
        ads = favorites + standards
        estate_list = []

        for ad in ads:
            ad_url = ad.select_one("a").get("href")
            ad_url = f"https://{ad_url[2:]}"
            layout_data = ad.select('div > a div div')[0].text.strip()
            
            ad_price = ad.select('div > a h3 span span')[1].text.strip()
            ad_housing_type = ad.select('div > a h3 span span')[0].text.strip()
            ad_location = ad.select('div > a h3 > span')[1].text.replace(" ", "").replace("\n", " ")

            ad_label = ad_housing_type
            ad_layout = f"{layout_data.split('•')[1].strip()} - {layout_data.split('•')[0].strip()}"
            ad_id = self.immo_id + "_" + ad.get("data-counter-id-value")

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

