import requests
from bs4 import BeautifulSoup

url = "https://www.century21-vu-villeurbanne-zola.com/annonces/achat/b-0-170000/p-3/"

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

ads = soup.select('div.tw-grid div.c-the-property-thumbnail-with-content[data-uid]')

for ad in ads:
    ad_id = ad.get('data-uid')
    ad_url = f"https://www.century21-vu-villeurbanne-zola.com/trouver_logement/detail/{ad_id}"
    ad_request = requests.get(ad_url)
    ad_soup = BeautifulSoup(ad_request.text, 'html.parser')
    price = ad_soup.select(".the-property-abstract__price")
    print(f"Price : {price}")