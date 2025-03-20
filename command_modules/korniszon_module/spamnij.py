
import os
import random
from typing import Optional
from selenium.webdriver.common.by import By
from selenium import webdriver
from utils import consts
from utils.utilities import wait_find_input_and_send_keys



class Spamnij():

    def __init__(self, database, driver: Optional[webdriver.Chrome] = None, wait_find_input_and_send_keys=wait_find_input_and_send_keys) -> None:

        self.database = database
        self.driver = driver
        self.wait_find_input_and_send_keys = wait_find_input_and_send_keys

        self.quantity = 1
        self.lenght = 1
        self.emotka = False
        self.exception_response = ""





    def _translate_input(self, input):

        parameters = input.split()
        
        print(f"input: {input}")
        print(f"parameters: {parameters}, len: {len(parameters)}")

        # remove emotka from input so input is a list is always beteewen 1 and 2
        if "emotka" in parameters:

            self.emotka = True
            parameters.remove("emotka")

        # check if input is a number
        if len(parameters) == 2:
            if parameters[0].isdigit() and parameters[1].isdigit():

                self.quantity = int(parameters[0])
                self.lenght = int(parameters[1])
            
            else:
                self.exception_response = "Pierwsze dwa inputy muszą być liczbowe :)."
                return True
            
        # if input is empty, return default values
        elif len(parameters) == 0:            
            return

        else:
            self.exception_response = "Dej dwa inputy z liczbami kierowniku <prosi>."
            return True





    # lenght - how many words in one spam
    # quantity - how many spams
    def spam_on_command(self, input, translate_input=None):

        #defauly values
        self.quantity = 1
        self.lenght = 1
        self.emotka = False


        if translate_input is None:
            translate_input = self._translate_input

        # also handles exceptions
        if translate_input(input):
            self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", self.exception_response)
            return


        quantity_limit = 10
        lenght_limit = 10

        table = os.getenv('MAIN_TABLE_NAME')
        query = f"""
                SELECT input
                FROM {table}
                ORDER BY RAND()
                LIMIT {self.lenght}
                """
        
        if self.quantity <= quantity_limit and self.lenght <= lenght_limit:
            for i in range(self.quantity):

                results = self.database.fetch(query) or []
                print(f"Spam: {results}")
                response = ' '.join(result[0] for result in results)
                
                if self.emotka:
                    emotka_str = f" {random.choice(consts.emotes)}"
                    response += emotka_str

                print(f"response: {response}")
                self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)

        else:
            response = f"Nie szalej typeczku <luzik>, max {quantity_limit}."
            self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)

