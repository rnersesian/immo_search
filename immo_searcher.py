from typing import List, Deque, Set
from immo_source import Estate, ImmoSource
from bot_telegram import BotTelegram
import csv
import time
from collections import deque

TIME_BTW_ANNOUNCES = 0.5
TIME_BTW_UPDATES = 300.0

class ImmoSearcher():

    def __init__(self, sources: List[ImmoSource], chatbot: BotTelegram, ads_file="estates.csv"):
        self.sources = sources
        self.broadcast_queue: Deque[Estate] = deque()
        self.existing_ids: Set[str] = set()
        
        self.announce_timer: float = 0
        self.update_timer: float = 0

        self.chatbot = chatbot
        self.estate_data_file = ads_file


        # Loading existing ids
        try:
            with open(self.estate_data_file, "r") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    self.existing_ids.add(row["id"])
        except FileNotFoundError as e:
            print(f"File not found : {e}")
            with open(self.estate_data_file, "w") as file:
                file.write("id;label;price;layout;location;url\n")

        print(self.existing_ids)


    def  run(self):
        last_time = time.perf_counter()
        
        while True:
            
            now = time.perf_counter()
            elapsed = now - last_time

            # Announcement management
            if self.announce_timer > 0:
                self.announce_timer -= elapsed

            elif len(self.broadcast_queue) > 0:
                estate_to_broadcast = self.broadcast_queue.popleft()
                self.broadcast_estate(estate_to_broadcast)
                self.announce_timer = TIME_BTW_ANNOUNCES

            # Data udpate management
            if self.update_timer > 0:
                self.update_timer -= elapsed

            else:
                print("Updating data")
                self.update_data()
                self.update_timer = TIME_BTW_UPDATES

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
                
        print(f"Number of estates found : {len(estates)}")
        # Removing estates already saved
        estates = [estate for estate in estates if estate.id not in self.existing_ids]
        print(f"After filtering: {len(estates)} new estates")

        if len(estates) > 0:
            self.save_estates(estates)
            
        for estate in estates:
            try:
                print(f"Adding to broadcast : {estate.id}")
                self.broadcast_queue.append(estate)
                self.existing_ids.add(estate.id)

            except Exception as e:
                print(f"Somethng went wrong : {e}")



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

    