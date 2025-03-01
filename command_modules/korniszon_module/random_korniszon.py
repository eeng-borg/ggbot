from selenium import webdriver
from selenium.webdriver.common.by import By
from command_modules.korniszon_module.leaderboard import Leaderboard
from utils.utilities import wait_find_input_and_send_keys
import random
import time
import threading
import os
import json


class SpamKorniszon:

    spam_time = 30
    spam_limit = 0



    def __init__(self, driver: webdriver.Chrome, leaderboard: Leaderboard) -> None:
        self.driver = driver
        self.leaderboard = leaderboard

        self.thread = None
        self.stop_event = threading.Event()

    

    def __spamming(self):

        while not self.stop_event.is_set():

            print(f'spamming: {SpamKorniszon.spam_time}')

            response = ''        
            for a in range(random.randint(1,3)):

                korniszon = random.choice(self.leaderboard.leaderboard)
                response += f"{korniszon['input']} "
            
            print(f"response: {response}")
            wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)

            time.sleep(SpamKorniszon.spam_time)



    # set new timer and start spamming
    def set_spamming_time(self, input=None, quiet=False):


        if input == None:

            with open("settings", 'r', encoding='utf-8') as f:
                settings = json.load(f)

            input_time = settings['spam_time']

        else:
            input_time = input




        try:
            new_spam_time = int(str(input_time))

            if new_spam_time > SpamKorniszon.spam_limit:
                
                
                SpamKorniszon.spam_time = new_spam_time * 60 # bcs minutes
              
                if self.thread == None:
                    self.thread = threading.Thread(target = self.__spamming, daemon=True) # starts the thread on main thread
                    self.thread.start() # do not exexutes

                if quiet == False:
                    response = f"Spam co {new_spam_time} minut (normalnych) <w8>"
                    wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)


        except ValueError:
            response = "Wprowadź liczbę kolego :)"
            wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)
            return




