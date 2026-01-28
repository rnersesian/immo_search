from . import ImmoSource, Estate
import requests
from bs4 import BeautifulSoup
from typing import List

class Century21(ImmoSource):

    def __init__(self, immo_id, base_url):
        super().__init__(immo_id)
        self.base_url = base_url
        self.ads_list_url = f"{self.base_url}/annonces/achat/b-0-160000/p-3/"
        self.ad_detail_url = f"{self.base_url}/trouver_logement/detail/"
    

    def update_data(self) -> List[Estate]:
        r = requests.get(self.ads_list_url, timeout=self.timeout_duration)
        soup = BeautifulSoup(r.text, 'html.parser')
        ads = soup.select('div.tw-grid div.c-the-property-thumbnail-with-content[data-uid]')
        estate_list = []
        
        for ad in ads:
            ad_id = ad.get('data-uid')
            ad_url = f"{self.ad_detail_url}/{ad_id}"
            # get detail page data
            ad_request = requests.get(ad_url)
            ad_soup = BeautifulSoup(ad_request.text, 'html.parser')

            # Getting ad information
            ad_header = ad_soup.select_one("div.c-the-property-abstract")
            title_info = ad_header.select('h1 span')

            # get info
            ad_price = ad_header.select("p.c-the-property-abstract__price")[0].text.strip()
            ad_label = title_info[0].text.strip()
            ad_layout = title_info[1].text.strip()
            ad_location = title_info[2].text.strip()
            ad_id = self.immo_id + ad_header.select("div > div > div")[0].text.split(":")[1].strip()

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

            
            