from typing import List
from immo_source import Estate, ImmoSource
from bot_telegram import BotTelegram
import csv
import time
import heapq

TIME_BTW_ANNOUCES = 0.5
TIME_BTW_UPDATES = 10.0

class ImmoSearcher():

    def __init__(self, sources: List[ImmoSource], chatbot: BotTelegram, ads_file="estates.csv"):
        self.sources = sources
        self.estate_queue: List[Estate] = []
        self.existing_ids: List[int] = []
        
        self.annouce_timer: float = 0
        self.update_timer: float = 0

        self.chatbot = chatbot


        # Loading existing ids
        try:
            with open(ads_file, "r") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    self.existing_ids.append(row["id"])
        except FileNotFoundError:
            with open(ads_file, "w") as file:
                file.write("id;label;price;layout;location;url\n")


    def run(self):
        last_time = time.perf_counter()
        estate_heap: List[Estate] = ["element A", "element B", "element C"]


        while True:
            
            now = time.perf_counter()
            elapsed = now - last_time

            if self.annouce_timer > 0:
                self.annouce_timer -= elapsed
            elif len(estate_heap) > 0:
                item = heapq.heappop(estate_heap)
                print(f"Anouncing {item}")
                self.annouce_timer = TIME_BTW_ANNOUCES

            if self.update_timer > 0:
                self.update_timer -= elapsed
            else:
                print("Updating data")
                self.update_timer = TIME_BTW_UPDATES

            last_time = now


    def update_data(self) -> List[Estate]:
        estates: List[Estate] = []
        for source in self.sources:
            more_estate = source.update_data()
            estates += more_estate

        estates = [estate for estate in estates if estate.id not in self.existing_ids]


    def broadcast_estate(self, estate: Estate):
        pass

    