import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from sql_database import Database
from command_modules.korniszon_module.leaderboard import Leaderboard
from datetime import datetime
from utils.utilities import wait_find_input_and_send_keys
from typing import Optional


class Topniszon:


    def __init__(self, database: Database, driver: Optional[webdriver.Chrome] = None, wait_find_input_and_send_keys=wait_find_input_and_send_keys):
        self.database = database
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
                return f"z {self.day_input} dnia tego miesiaca"
        
        except ValueError:
            response = "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiaca chciałbyś topniszona, np /topniszon 5."
            self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)

            # for tests mainly
            return response




    def best_korniszon_by_day(self, day_input, best=True, datetime_now=datetime.now()):

        self.day_input = day_input
        when = ''


        # check if input is a number, otherwise throw exception message
        when = self._input_to_when(day_input, datetime_now)
        print(f"Day: {self.day_input}")


        # so return is always a string
        response = ''


        year_now = datetime_now.year
        month_now = datetime_now.month
        table = os.getenv('MAIN_TABLE_NAME')

        view_name = ''
        if best:
            view_name = 'topniszon'
        else:
            view_name = 'worstniszon'


        query = f"""
                SELECT *
                FROM {table}_{view_name}
                WHERE created LIKE %s
                ORDER BY created DESC
                """
        date_pattern = f"{year_now}-{month_now:02d}-{self.day_input:02d}%"
        print(f"Searching with date pattern: {date_pattern}")
        topek = self.database.fetch(query, params=(date_pattern,), fetch_one=True, dictionary=True)
        
        if topek is None:
            response = f"Niczego tutaj nie znajdę dla {when} <bezradny>"
            self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)
            return response


        response = ''
        

        if best is True:
            response = f"Najlepszy {when} <paker>\n"
        else:
            response = f"Najgorszy {when} <wyśmiewacz>\n"


        position = topek['position']
        input = topek['input']
        score = topek['score']
        user = topek['user']

        created_dt = topek['created']
        hour = created_dt.hour
        minute = created_dt.minute


        response += f"{position}. {input} - {score} ({user}) o {hour}:{minute:02d}"


        self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)
        return response