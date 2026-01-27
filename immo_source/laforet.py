from . import ImmoSource, Estate
import requests
from bs4 import BeautifulSoup

class Laforet(ImmoSource):
    
    def __init__(self, immo_id, base_url):
        super().__init__(immo_id)
        self.ads_list_url = f"{base_url}/acheter?filter[max]=180000&filter[rooms]=3"

    def update_data(self):
        r = requests.get(self.ads_list_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        favorites = soup.select("div#favoriz--page--1 article")
        standards = soup.select("div#standard--page--1 article")
        ads = favorites + standards

        for ad in ads:
            ad_url = "https://www.laforet.com" + ad.select_one("a").get("href")
            layout_data = ad.select('div > a div div')[0].text.strip()
            
            ad_price = ad.select('div > a h3 span span')[1].text.strip()
            ad_housing_type = ad.select('div > a h3 span span')[0].text.strip()
            ad_location = ad.select('div > a h3 > span')[1].text.replace(" ", "").replace("\n", " ")

            ad_label = ad_housing_type
            ad_layout = f"{layout_data.split('•')[0].strip()} - {layout_data.split('•')[1].strip()}"
            ad_id = self.immo_id + "_" + ad.get("data-counter-id-value")

            estate = Estate(
                id=ad_id,
                label=ad_label,
                price=ad_price,
                layout=ad_layout,
                location=ad_location
            )
            estate.save()
