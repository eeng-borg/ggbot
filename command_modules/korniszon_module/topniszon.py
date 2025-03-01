from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.types import CommandData
from command_modules.korniszon_module.leaderboard import Leaderboard
from datetime import datetime
from utils.utilities import wait_find_input_and_send_keys
from typing import Optional


class Topniszon:


    def __init__(self, driver: Optional[webdriver.Chrome] = None, wait_find_input_and_send_keys=wait_find_input_and_send_keys):
        self.driver = driver
        self.day_input = None
        self.wait_find_input_and_send_keys = wait_find_input_and_send_keys



    def _input_to_when(self, input, datetime_now=datetime.now()):

        try:
            if input == '':
                self.day_input = datetime_now.day
                return 'dziś'

            else:
                self.day_input = int(input)
                return f"z {self.day_input} dnia tego miesiąca"
        
        except ValueError:
            response = "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."
            self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)

            # for tests mainly
            return response




    def best_korniszon_by_day(self, input, leaderboard: Leaderboard, best=True, datetime_now=datetime.now()):

        self.day_input = input
        when = ''


        # check if input is a number, otherwise throw exception message
        when = self._input_to_when(input, datetime_now)
        print(f"Day: {self.day_input}")


        # so return is always a string
        response = ''
        _leaderboard = leaderboard.leaderboard

        if best is False:
            _leaderboard = list(reversed(leaderboard.leaderboard))



        for korniszon in _leaderboard:

            # if input is empty, then lets assume that user wants the best one from today
            # if day_input == '':

            if korniszon['timestamp'] != None:
                
                # convert timestamp to datetime object for better handling
                timestamp = korniszon['timestamp']
                korniszon_datetime = datetime.fromtimestamp(timestamp)

                if korniszon_datetime.day == self.day_input and korniszon_datetime.month == datetime_now.month and korniszon_datetime.year == datetime_now.year:
                    # can't really say which one at 0 score is the worst, so instead we are counting the worst one that scored any points
                    if korniszon['score'] > 0:
                        
                        position = korniszon.get('position')
                        input = korniszon.get('input')
                        score = korniszon.get('score')
                        user = korniszon.get('user')

                        hour = korniszon_datetime.hour
                        minute = korniszon_datetime.minute

                        response = ""
                        

                        if best is True:
                            response = f"Najlepszy {when} <paker>\n"
                        else:
                            response = f"Najgorszy {when} <wyśmiewacz>\n"


                        response += f"{position}. {input} - {score} ({user}) o {hour}:{minute:02d}"


                        self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)
                        return response