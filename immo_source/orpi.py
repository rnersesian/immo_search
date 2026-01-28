from . import ImmoSource, Estate
import requests
from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
from typing import List

class Orpi(ImmoSource):
    def __init__(self, immo_id, base_url="https://www.orpi.com", ):
        super().__init__(immo_id)
        self.base_url = base_url
        self.ads_list_url = self.base_url + '/recherche/buy?transaction=buy&resultUrl=&realEstateTypes%5B0%5D=maison&realEstateTypes%5B1%5D=appartement&locations%5B0%5D%5Bvalue%5D=lyon&locations%5B0%5D%5Blabel%5D=Lyon&locations%5B0%5D%5Blatitude%5D=45.758&locations%5B0%5D%5Blongitude%5D=4.83494&locations%5B1%5D%5Bvalue%5D=tassin-la-demi-lune&locations%5B1%5D%5Blabel%5D=Tassin-la-Demi-Lune%20%2869160%29&locations%5B1%5D%5Blatitude%5D=45.7635&locations%5B1%5D%5Blongitude%5D=4.75077&locations%5B2%5D%5Bvalue%5D=oullins&locations%5B2%5D%5Blabel%5D=Oullins%20%2869310%29&locations%5B2%5D%5Blatitude%5D=45.7142&locations%5B2%5D%5Blongitude%5D=4.80072&locations%5B3%5D%5Bvalue%5D=villeurbanne&locations%5B3%5D%5Blabel%5D=Villeurbanne%20%2869100%29&locations%5B3%5D%5Blatitude%5D=45.7722&locations%5B3%5D%5Blongitude%5D=4.89036&locations%5B4%5D%5Bvalue%5D=la-mulatiere&locations%5B4%5D%5Blabel%5D=La%20Mulati%C3%A8re%20%2869350%29%20-%20Ville&locations%5B4%5D%5Blatitude%5D=45.734&locations%5B4%5D%5Blongitude%5D=4.81165&agency=&minSurface=&maxSurface=&minLotSurface=&maxLotSurface=&minStoryLocation=&maxStoryLocation=&numbersOfRooms%5B0%5D=3&newBuild=&oldBuild=&lifeAnnuity=&minPrice=&maxPrice=160000&sort=date-down&layoutType=list&recentlySold=false&searchRange='
        

    def update_data(self) -> List[Estate]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.ads_list_url)
            
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, 'html.parser')
        ads = soup.select('ul.c-results__list')[0].select('li.c-results__list__item > article')
        estate_list = []

        for ad in ads:
            # Getting price
            ad_price = ad.select_one('div.c-estate-thumb__details div.c-estate-thumb__price-tag > span.c-estate-thumb__price-tag__price').text.replace(" ", "").replace("\n" , " ")
            ad_price = ad_price[:-1] + " €"

            basic_info = ad.select('div.c-estate-thumb__infos__estate > a.c-overlay__link > b')[0]
            # Gettng layout information
            surface =  basic_info.select('span')[1].text.replace(" ", "").replace("\n", " ")
            match = re.search(r'\d+\s*pièces?', basic_info.text)
            nb_rooms = match.group() if match else "? pièces"
            ad_layout = f"{nb_rooms} - {surface}"

            # Getting url
            ad_url = "https://www.orpi.com" + ad.select('div.c-estate-thumb__infos__estate > a.c-overlay__link')[0].get('href')
            # Getting label
            ad_label = basic_info.select("span")[0].text.replace(" ", "").replace('Achat\n', '')
            # Getting location
            ad_location = ad.select_one('div.c-estate-thumb__infos span.c-estate-thumb__infos__location').text.replace("  ", "").replace("\n", "")
            ad_id = f"{self.immo_id}_{ad.get("id")}"

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

