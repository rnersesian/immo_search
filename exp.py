import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json

url = "https://api.eraimmobilier.com/api/v2/annonces/search?page=1&type_annonce=vente&nb_pieces=3&prix_to=440000&per_page=8&order_dir=desc&statut=0,1,11&agence_id=262"





from immo_source.era_immobilier import EraImmobilier


source = EraImmobilier(immo_id="ERA_Lyon3", agency_id=262)
source.update_data()