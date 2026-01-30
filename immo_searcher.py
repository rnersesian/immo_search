from typing import List, Deque, Set
from immo_source import Estate, ImmoSource
from bot_telegram import BotTelegram
import csv
import time
import random
from collections import deque
from datetime import datetime
import math

TIME_BTW_ANNOUNCES = 3.0
MIN_TIME_BTW_UPDATE = 5400
MAX_TIME_BTW_UPDATES = 9000

def is_quiet_hours() -> bool:
    """Check if quiet hours"""
    hour = datetime.now().hour
    return hour >= 21 or hour < 8

class ImmoSearcher():

    def __init__(self, sources: List[ImmoSource], chatbot: BotTelegram, ads_file="estates.csv"):
        self.sources = sources
        self.broadcast_queue: Deque[Estate] = deque()
        self.existing_urls: Set[str] = set()
        
        self.announce_timer: float = 0
        self.update_timer: float = 0

        self.chatbot = chatbot
        self.estate_data_file = ads_file


        # Loading existing ids
        try:
            with open(self.estate_data_file, "r") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    self.existing_urls.add(row["url"])
        except FileNotFoundError as e:
            print(f"File not found : {e}")
            with open(self.estate_data_file, "w") as file:
                file.write("id;label;price;layout;location;url\n")

        print(self.existing_urls)


    def  run(self):
        last_time = time.perf_counter()
        
        while True:
            if is_quiet_hours():
                print("Is quiet hour, sleeping")
                time.sleep(60)  # Vérifie toutes les minutes pendant la nuit
                continue

            now = time.perf_counter()
            elapsed = now - last_time

            # Announcement management
            if self.announce_timer > 0:
                self.announce_timer -= elapsed

            elif len(self.broadcast_queue) > 0:
                estate_to_broadcast = self.broadcast_queue.popleft()
                print(f"\n############ BROADCASTING -> {estate_to_broadcast.id}")
                print(f"#### URL -> {estate_to_broadcast.url}")
                print(f"#### Broadcast in queue : {len(self.broadcast_queue)}\n")
                self.broadcast_estate(estate_to_broadcast)
                self.announce_timer = TIME_BTW_ANNOUNCES

            # Data udpate management
            if self.update_timer > 0:
                self.update_timer -= elapsed

            else:
                print("Updating data")
                self.update_data()
                udpate_delay =  float(math.floor(random.uniform(MIN_TIME_BTW_UPDATE, MAX_TIME_BTW_UPDATES)))
                print(f"Waiting for {udpate_delay} seconds before next udpate")
                self.update_timer = udpate_delay

            last_time = now


    def update_data(self) -> List[Estate]:
        """Gathering estate ads from sources"""
        estates: List[Estate] = []

        for source in self.sources:
            try:
                more_estate = source.update_data()
                estates += more_estate
            except Exception as e:
                # Notify on telegram is something wrong
                self.broadcast_error(f"Problème avec l'agence \n {source.immo_id}")
                print(f"Error from {source.immo_id}: {type(e).__name__}: {e}")
            
            # random delay between calls to avoid suspicions 1 - 3 seconds
            delay = random.uniform(1,3)
            time.sleep(delay)

        
                
        print(f"Number of estates found : {len(estates)}")
        # Removing estates already saved
        estates
        estates_to_save: List[Estate] = []
            
        for estate in estates:
            # Not checking by id because of crossposting
            if estate.url not in self.existing_urls:
                try:
                    print(f"Adding to broadcast : {estate.url}")
                    self.broadcast_queue.append(estate)
                    self.existing_urls.add(estate.url)
                    estates_to_save.append(estate)

                except Exception as e:
                    print(f"Somethng went wrong : {e}")

        if len(estates_to_save) > 0:
            self.save_estates(estates_to_save)



    def save_estates(self, estates: List[Estate]):
        with open(self.estate_data_file, "a", newline='') as f:
            writer = csv.writer(f, delimiter=";")
            for estate in estates:
                writer.writerow([estate.id, estate.label, estate.price, estate.layout, estate.location, estate.url])


    def broadcast_estate(self, estate: Estate):
        try:
            self.chatbot.post_request("/sendMessage", data={
                "chat_id": self.chatbot.chat_id,
                "text": estate.format_to_message(),
                "parse_mode": "HTML"
            })
        except Exception as e:
            print(f"Somethng went wrong : {e}")


    def broadcast_error(self, mesasge):
        self.chatbot.send_error(mesasge)

    