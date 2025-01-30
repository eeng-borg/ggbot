from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from command_modules.korniszon_module.leaderboard import Leaderboard
from utils.utilities import async_wait_find_input_send_keys
import asyncio
import random


async def post_random_korniszon(driver: webdriver.Chrome, leaderboard: Leaderboard, spam = 200):

    await asyncio.sleep(spam) #900
    leaderboard.load_leaderboard()
    korniszon = random.choice(leaderboard.leaderboard)
    response = korniszon['input']
    
    await async_wait_find_input_send_keys(driver, 1, By.ID, "chat-text", response)




