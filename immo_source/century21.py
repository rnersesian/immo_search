from . import ImmoSource, Estate
import requests
from bs4 import BeautifulSoup
from typing import List

class Century21(ImmoSource):

    def __init__(self, immo_id, base_url):
        super().__init__(immo_id)
        self.base_url = base_url
        self.ads_list_url = f"{self.base_url}/annonces/achat/b-0-160000/p-3/"
        self.ad_detail_url = f"{self.base_url}/trouver_logement/detail"
    

    def update_data(self) -> List[Estate]:
        r = requests.get(self.ads_list_url, timeout=self.timeout_duration)
        soup = BeautifulSoup(r.text, 'html.parser')
        ads = soup.select('div.tw-grid div.c-the-property-thumbnail-with-content[data-uid]')
        ads_info = soup.select('div.c-the-property-thumbnail-with-content__col-right > h3 > div')

        estate_list = []
        
        for i in range(len(ads)):
            ad_id = ads[i].get('data-uid')
            ad_url = f"{self.ad_detail_url}/{ad_id}"
            ad_location = ads_info[i*2].contents[0].text.strip().replace("  ", "")
            ad_layout = ads_info[i*2].contents[2].text.strip() + "²" + ads_info[i*2].contents[4].text.strip()
            ad_label = ads_info[i*2 + 1].select("div.c-text-theme-heading-3")[0].text.strip()
            ad_price = ads_info[i*2 + 1].select("div")[1].text.strip()

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

            
            