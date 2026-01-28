import requests
from bs4 import BeautifulSoup
import re

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# }

url = 'https://www.orpi.com/recherche/buy?transaction=buy&resultUrl=&realEstateTypes%5B0%5D=maison&realEstateTypes%5B1%5D=appartement&locations%5B0%5D%5Bvalue%5D=lyon&locations%5B0%5D%5Blabel%5D=Lyon&locations%5B0%5D%5Blatitude%5D=45.758&locations%5B0%5D%5Blongitude%5D=4.83494&locations%5B1%5D%5Bvalue%5D=tassin-la-demi-lune&locations%5B1%5D%5Blabel%5D=Tassin-la-Demi-Lune%20%2869160%29&locations%5B1%5D%5Blatitude%5D=45.7635&locations%5B1%5D%5Blongitude%5D=4.75077&locations%5B2%5D%5Bvalue%5D=oullins&locations%5B2%5D%5Blabel%5D=Oullins%20%2869310%29&locations%5B2%5D%5Blatitude%5D=45.7142&locations%5B2%5D%5Blongitude%5D=4.80072&locations%5B3%5D%5Bvalue%5D=villeurbanne&locations%5B3%5D%5Blabel%5D=Villeurbanne%20%2869100%29&locations%5B3%5D%5Blatitude%5D=45.7722&locations%5B3%5D%5Blongitude%5D=4.89036&locations%5B4%5D%5Bvalue%5D=la-mulatiere&locations%5B4%5D%5Blabel%5D=La%20Mulati%C3%A8re%20%2869350%29%20-%20Ville&locations%5B4%5D%5Blatitude%5D=45.734&locations%5B4%5D%5Blongitude%5D=4.81165&agency=&minSurface=&maxSurface=&minLotSurface=&maxLotSurface=&minStoryLocation=&maxStoryLocation=&numbersOfRooms%5B0%5D=3&newBuild=&oldBuild=&lifeAnnuity=&minPrice=&maxPrice=160000&sort=date-down&layoutType=list&recentlySold=false&searchRange='

# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)
#     page = browser.new_page()
#     page.goto(url)
immo_id = "ORPI"
    
#     html = page.content()
with open("test.html", "r") as file:
    html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.select('ul.c-results__list')[0].select('li.c-results__list__item > article')
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
        ad_id = f"{immo_id}_{ad.get("id")}"

        print(f"ID : {ad_id}")
        print(f"Price : {ad_price}")
        print(f"URL : {ad_url}")
        print(f"Layout : {ad_layout}")
        print(f"Label : {ad_label}")
        print(f"Location : {ad_location}")