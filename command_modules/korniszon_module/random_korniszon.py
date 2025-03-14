from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from command_modules.korniszon_module.leaderboard import Leaderboard
from utils.utilities import wait_find_input_and_send_keys
from sql_database import Database
import random
import time
import threading
import json
import os



class SpamKorniszon:


    def __init__(self, database: Database, driver: webdriver.Chrome, leaderboard: Leaderboard, wait_find_input_and_send_keys=wait_find_input_and_send_keys) -> None:
        
        self.database = database
        self.driver = driver
        self.leaderboard = leaderboard
        self.wait_find_input_and_send_keys = wait_find_input_and_send_keys

        self.thread = None
        self.stop_event = threading.Event()

        self.spam_time = 30
        self.spam_limit = 0
        self.spam_time_left = 0
        self.keep_spamming = True # emergence

        self.set_spamming_time(quiet=True)




    def _spamming(self):

        while self.keep_spamming:

            time.sleep(1)
            self.spam_time_left -= 1
            # print(f"Time left: {self.spam_time_left}")

            if self.spam_time_left < 0:

                count = random.randint(1, 3)
                query = f"""
                    SELECT input 
                    FROM (
                        SELECT input
                        FROM korniszons_test 
                        ORDER BY RAND()
                        LIMIT {count}
                    ) t
                """
                results = self.database.fetch(query) or []
                response = ' '.join(result[0] for result in results)
                
                print(f"response: {response}")
                self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)
                
                self.spam_time_left = self.spam_time




    def _create_file_if_none(self, file_name, dict):
        # if no settings file exist, create one with default spam_time
        if not os.path.exists(file_name):

            print("JSON nie istnije!!")
            with open(file_name, 'w', encoding='utf-8') as f:
                
                dict['spam_time'] = 41
                json.dump(dict, f, indent=4)




    def _get_spam_time(self, file_name, input):

        with open(file_name, 'r', encoding='utf-8') as f:

            settings_json = json.load(f)

        if input == None:
            spam_time = settings_json['spam_time']
            return spam_time

        else:
            spam_time = int(input)
            settings_json['spam_time'] = spam_time

            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(settings_json, f, indent=4)
            
            return spam_time




    # set new timer and start spamming
    def set_spamming_time(self, quiet=False, input=None):

        settings_name = "settings.json"
        settings_json = {}

        # if no settings file exist, create one with default spam_time
        self._create_file_if_none(settings_name, settings_json)


        try:
            spam_time = self._get_spam_time(settings_name, input)

        except ValueError:
            response = "Wprowadz liczbę kolego :)"
            self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)
            return



        # wczytywanie i zapisywanie spam_time w settings.json        
        new_spam_time = int(str(spam_time))
        

        if new_spam_time > self.spam_limit:
            
            self.spam_time = new_spam_time * 60 # bcs minutes
            self.spam_time_left = self.spam_time
            print(f'spamming: {self.spam_time}')
            
            if self.thread == None:
                self.thread = threading.Thread(target = self._spamming, daemon=True) # starts the thread on main thread
                self.thread.start() # do not exexutes


            if quiet == False:
                response = f"Spam co {new_spam_time} minut (normalnych) <w8>"
                self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)






