from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.types import CommandData
from command_modules.korniszon_module.leaderboard import Leaderboard
from datetime import datetime
from utils.utilities import wait_find_input_and_send_keys
from typing import Optional


class Topniszon:


    def __init__(self, driver: Optional[webdriver.Chrome] = None):
        self.driver = driver
        self.day_input = None



    def _input_to_when(self, input, wait_find_input_and_send_keys=wait_find_input_and_send_keys):

        try:
            if input == '':
                self.day_input = datetime.now().day
                return 'dziś'

            else:
                self.day_input = int(input)
                return f"z {self.day_input} dnia tego miesiąca"
        
        except ValueError:
            response = "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."
            wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)

            # for tests mainly
            return response




    def best_korniszon_by_day(self, data: CommandData, leaderboard: Leaderboard, wait_find_input_and_send_keys=wait_find_input_and_send_keys):

        input = data.get('input')
        self.day_input = input

        when = ''


        # check if input is a number, otherwise throw exception message
        when = self._input_to_when(input)

        # so return is always a string
        response = ''
        
        for korniszon in reversed(leaderboard.leaderboard):

            # if input is empty, then lets assume that user wants the best one from today
            # if day_input == '':

            if korniszon['time'] != None:
                if korniszon['time']['day'] == self.day_input and korniszon['time']['month'] == datetime.now().month and korniszon['time']['year'] == datetime.now().year:

                            position = korniszon.get('position')
                            input = korniszon.get('input')
                            score = korniszon.get('score')
                            user = korniszon.get('user')

                            time = korniszon.get('time')
                            hour = time.get('hour')
                            minute = time.get('minute')



                            response = f"Najlepszy {when} <paker>\n"
                            response += f"{position}. {input} - {score} ({user}) o {hour}:{minute:02d}"


        return wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)