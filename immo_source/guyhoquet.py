from . import ImmoSource, Estate
import requests
from bs4 import BeautifulSoup
from typing import List
from playwright.sync_api import sync_playwright
import atexit

class GuyHoquet(ImmoSource):

    def __init__(self, immo_id, base_url):
        super().__init__(immo_id)
        self.base_url = base_url
        self.ads_list_url = f"{self.base_url}/biens/result#1&p=1&f10=1&f40=160000&f70=3"


    def update_data(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.ads_list_url)
            page.wait_for_timeout(2500)

            html = page.content()
            browser.close()
        
        soup = BeautifulSoup(html, "html.parser")
        ads = soup.select("div.results-search > div.section-content > div.resultat-item")

        estate_list: List[Estate] = []
    
        for ad in ads:
            basic_info = ad.select("span.property-name")[0].text.strip().replace("  ", "").split("\n")
            ad_label = basic_info[0]
            ad_layout = f"{basic_info[1]} - {basic_info[2]}".replace("  ", " ")
            ad_id = ad.get("data-id")
            ad_url = ad.select_one("a").get("href")
            ad_price = ad.select_one("div.price").text.strip()
            ad_location = ad.select_one("div.resultat-info div[title]").get("title")
    
            
            estate_list.append(
                Estate(
                    id=f"{self.immo_id}_{ad_id}",
                    label=ad_label,
                    price=ad_price,
                    layout=ad_layout,
                    location=ad_location,
                    url=ad_url
            ))
        return estate_list