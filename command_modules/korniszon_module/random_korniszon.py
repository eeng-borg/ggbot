from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from command_modules.korniszon_module.leaderboard import Leaderboard
from utils.utilities import async_wait_find_input_send_keys, wait_find_input_and_send_keys
import asyncio
import random
import time

class SpamKorniszon:

    spam_time = 30
    counting = 0


    def spamming(self, driver: webdriver.Chrome, leaderboard: Leaderboard):

        SpamKorniszon.counting += 1/30
        # print(f"Minął czas: {SpamKorniszon.counting} > {SpamKorniszon.spam_time}")

        if SpamKorniszon.counting > SpamKorniszon.spam_time:

            leaderboard.load_leaderboard()
            
            response = ''
            
            for a in range(random.randint(1,3)):
                korniszon = random.choice(leaderboard.leaderboard)
                response += f"{korniszon['input']} "
            
            wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", response)

            SpamKorniszon.counting = 0




