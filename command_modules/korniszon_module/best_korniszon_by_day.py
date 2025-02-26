from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.types import CommandData
from command_modules.korniszon_module.leaderboard import Leaderboard
from datetime import datetime
from utils.utilities import wait_find_input_and_send_keys, wait_find_and_return, wait_find_and_click, clear_chat, filter_bmp


def best_korniszon_by_day(driver: webdriver.Chrome, data: CommandData, leaderboard: Leaderboard):

    input = data.get('input')
    day_input = input

    string_when = ''


    # check if input is a number, otherwise throw exception message
    try:
        if input == '':
            day_input = datetime.now().day
            string_when = 'dziś'

        else:
            day_input = int(input)
            string_when = f"z {day_input} dnia tego miesiąca"
    
    except ValueError:
        response = "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."
        wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", response)



    response = ''
    
    for korniszon in reversed(leaderboard.leaderboard):

        # if input is empty, then lets assume that user wants the best one from today
        # if day_input == '':

        if korniszon['time'] != None:
            if korniszon['time']['day'] == day_input:
                if korniszon['time']['month'] == datetime.now().month:
                    if korniszon['time']['year'] == datetime.now().year:

                        position = korniszon.get('position')
                        input = korniszon.get('input')
                        score = korniszon.get('score')
                        user = korniszon.get('user')

                        time = korniszon.get('time')
                        hour = time.get('hour')
                        minute = time.get('minute')



                        response = f"Najlepszy {string_when} <paker>\n"
                        response += f"{position}. {input} - {score} ({user}) o {hour}:{minute:02d}"

        # else:
        #     if korniszon['time']['day'] == day_input:

        #         position = korniszon.get('position')
        #         input = korniszon.get('input')
        #         response = f"{position}. {input}"


    return wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", response)