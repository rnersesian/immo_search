import requests
from bs4 import BeautifulSoup

url = "https://www.century21-dauphine-lacassagne-lyon.com/annonces/achat-appartement/"

with open("test.html", "r") as file:
    soup = BeautifulSoup(file.read(), "html.parser")
    ads = soup.select('div.tw-grid div.c-the-property-thumbnail-with-content[data-uid]')
    ads_info = soup.select('div.c-the-property-thumbnail-with-content__col-right > h3 > div')
    
    for i in range(len(ads)):
        # header_info = ads_info[i*2]
        ad_id = ads[i].get('data-uid')
        ad_location = ads_info[i*2].contents[0].text.strip().replace("  ", "")
        ad_layout = ads_info[i*2].contents[2].text.strip() + "²" + ads_info[i*2].contents[4].text.strip()
        ad_label = ads_info[i*2 + 1].select("div.c-text-theme-heading-3")[0].text.strip()
        ad_price = ads_info[i*2 + 1].select("div")[1].text.strip()

        print(f"ID: {ad_id}")
        print(f"Location : {ad_location}")
        print(f"Layout : {ad_layout}")
        print(f"Label : {ad_label}")
        print(f"Price : {ad_price}")
        print()
    print(len(ads))
    print(f"Ads info length : {len(ads_info)}")