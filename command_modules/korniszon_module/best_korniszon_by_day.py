from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.types import CommandData
from command_modules.korniszon_module.leaderboard import Leaderboard
from datetime import datetime
from utils.utilities import wait_find_input_and_send_keys, wait_find_and_return, wait_find_and_click, clear_chat, filter_bmp


def best_korniszon_by_day(driver: webdriver.Chrome, data: CommandData, leaderboard: Leaderboard):

    clear_chat(driver)

    day_input = data.get('input')
    response = ''
    
    for korniszon in reversed(leaderboard.leaderboard):

        # if input is empty, then lets assume that user wants the best one from today
        # if day_input == '':

        if korniszon['time']['day'] == datetime.now().day:
            if korniszon['time']['month'] == datetime.now().month:
                if korniszon['time']['year'] == datetime.now().year:

                    position = korniszon.get('position')
                    input = korniszon.get('input')
                    score = korniszon.get('score')
                    user = korniszon.get('user')

                    time = korniszon.get('time')
                    hour = time.get('hour')
                    minute = time.get('minute')

                    response = "Najlepszy dziś <paker>\n"
                    response += f"{position}. {input} - {score} ({user}) o {hour}:{minute:02d}"

        # else:
        #     if korniszon['time']['day'] == day_input:

        #         position = korniszon.get('position')
        #         input = korniszon.get('input')
        #         response = f"{position}. {input}"


    return wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", response)