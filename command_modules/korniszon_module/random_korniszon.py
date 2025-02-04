from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from command_modules.korniszon_module.leaderboard import Leaderboard
from utils.utilities import async_wait_find_input_send_keys, wait_find_input_and_send_keys
import asyncio
import random
import time

class SpamKorniszon:

    spam_time = 10
    counting = 0
    spam_limit = 0


    def spamming(self, driver: webdriver.Chrome, leaderboard: Leaderboard):

        SpamKorniszon.counting += 1/120
        # print(f"Minął czas: {SpamKorniszon.counting} > {SpamKorniszon.spam_time}")

        if SpamKorniszon.counting > SpamKorniszon.spam_time:

            # leaderboard.load_leaderboard()
            
            response = ''
            
            for a in range(random.randint(1,3)):
                korniszon = random.choice(leaderboard.leaderboard)
                response += f"{korniszon['input']} "
            
            wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", response)

            SpamKorniszon.counting = 0


    def set_spamming_time(self, driver: webdriver.Chrome, command_data):

        try:
            new_spam_time = int(command_data['input'])
            print(f"spam: {new_spam_time}")

            if new_spam_time > SpamKorniszon.spam_limit:
                SpamKorniszon.spam_time = new_spam_time
                print(f"spam korniszon: {new_spam_time}")
                response = f"Spam co {new_spam_time} pseudo minut <w8>"
                wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", response)

        except ValueError:
            pass




