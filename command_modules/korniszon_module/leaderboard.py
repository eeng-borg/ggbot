from utils.utilities import wait_find_input_and_send_keys, wait_find_and_return, wait_find_and_click, clear_chat, filter_bmp
from utils.types import CommandData, KorniszonData
import json
import os
import math
from selenium.webdriver.common.by import By
from selenium import webdriver
import logging as log


# korniszon leaderboard
class Leaderboard:

    leaderboard_file_name = "leaderboard_new.json"
    leaderboard = []

    def load_leaderboard(self):

        # check if file exists already, if not made one
        if not os.path.exists(self.leaderboard_file_name):
            print("JSON nie istnije!!")

            # Save dict to a JSON file if it doesn't exist
            with open(self.leaderboard_file_name, 'w', encoding='utf-8') as f:
                json.dump(self.leaderboard, f, indent=4)

        # load dict from a JSON file        
        try:
            with open(self.leaderboard_file_name, 'r', encoding='utf-8') as f:
                self.leaderboard = json.load(f)

        except json.JSONDecodeError:
            print("Błąd JSON! Resetuję leaderboard.")
            # self.leaderboard = {}


    def add_korniszon(self, command_data: CommandData, score: float):

        new_korniszon = {}

        # add score to new_korniszon data and remove command type
        for data_key, data_value in command_data.items():
            new_korniszon[data_key] = data_value

        del new_korniszon['command']


        new_korniszon["score"] = score
        del new_korniszon["command"]

        # add new result
        self.leaderboard.append(new_korniszon)


        # print(f"add new result:  {self.leaderboard}")

        # sort
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x.get('score', 0), reverse=True) # print(sorted_leaderboard)
        
        # Save to a JSON file
        with open(self.leaderboard_file_name, 'w', encoding='utf-8') as f:
            # print(f"Zapisuje: {sorted_leaderboard}")
            json.dump(sorted_leaderboard, f, indent=4 )

        
        self.leaderboard = sorted_leaderboard
    
    
    def get_position(self, korniszon_text: str) -> int | None:

        # Convert dict keys to a list and find index to determine it's position on leaderboard
        # new_korniszon returns leaderboard_sorted

        for item in self.leaderboard:
            log.info(f"Item: {item}")

            if item.get("input") == korniszon_text:
                position = self.leaderboard.index(item) + 1
                print(f"position: {position}")

                return position

        
    
    # def find_by_name(self, korniszon_text):
    #     self.leaderboard

    def display_leaderboard(self, driver: webdriver.Chrome, data_input: str):

        # from_index = 0
        # to_index = 10
        # if data_input:
        #     # remove everything except numbers and spaces
        #     numbers = "".join([char for char in data_input if char.isdigit() or char.isspace()])
        #     input_list = numbers.split(" ")
        #     print(f"input_list: {len(input_list)}")

        #     if len(input_list) == 2:
        #         from_index = int(input_list[0])
        #         to_index = int(input_list[1])

        #     elif len(input_list) == 1:
        #         to_index = int(input_list[0])

        # for index, korniszon in enumerate(self.leaderboard[from_index : to_index]):
        for index, korniszon in enumerate(self.leaderboard[:10]):

            input = korniszon.get("input")
            score = korniszon.get("score")
            user = korniszon.get("user")

            if len(self.leaderboard) > 0:

                response = f"{index + 1}. {input} - {score}"
                if user:
                    response += f" ({user})"

                wait_find_input_and_send_keys(driver, 10, By.ID, "chat-text", response)
            else:
                response = "Nic tu nie ma, zrób najpierw jakieś korniszony może :)"
                wait_find_input_and_send_keys(driver, 10, By.ID, "chat-text", response)
        
        clear_chat(driver)

    # -------------------------

    # user stats

    def __get_user_score_sum(self, user: str) -> float:

        score_sum = 0

        for korniszon in self.leaderboard:
            if korniszon.get("user") == user:
                score = korniszon.get("score")
                score_sum += score

        return score_sum
    
    
    def __get_user_average_score(self, user: str) -> float:

        score_sum = self.__get_user_score_sum(user)
        score_average = 0
        index = 0

        for korniszon in self.leaderboard:
            if korniszon.get("user") == user:
                index += 1

        score_average = score_sum / index

        return score_average
    

    def ___get_user_korniszons(self, user: str, how_many = float('inf')) -> list[str]: # get infinite float and convert it to int and assign it if how_many is not given
        
        korniszons = []
        ammount = 0

        for index, korniszon in enumerate(self.leaderboard):
            if korniszon.get("user") == user:

                place = index + 1
                input = korniszon.get("input")
                score = korniszon.get("score")
                
                korniszons.append(f"{place}. {input} - {score}")

                if ammount >= how_many:
                    break
                
                ammount += 1
        
        return korniszons


    # user functions
    def display_user_stats(self, driver: webdriver.Chrome, user: str):
        
        clear_chat(driver)

        # check if user has any korniszon, if not then he don't have any stats to show
        # is_at_least_one = self.___get_user_korniszons(user, 1)

        if self.___get_user_korniszons(user, 1):

            score_sum = self.__get_user_score_sum(user)
            score_average = self.__get_user_average_score(user)
            best_tree = self.___get_user_korniszons(user, 2)
            quantity = len(self.___get_user_korniszons(user))


            print(f"Top tree: {best_tree}")
            print(f"Top 0: {best_tree[0]}")

            # display user stats
            response = (
                f"-- STATYSTKI {user} --\n"
                f"Łącznie zdobytych punktów: {round(score_sum, 2)}\n"
                f"Średnia punktów: {round(score_average, 2)}\n"
                f"Ilość korniszonów: {quantity}\n"
                f"Top 3 korniszonów:\n"
            )
            response += "\n".join(best_tree)

            return wait_find_input_and_send_keys(driver, 10, By.ID, "chat-text", response)
            
        else:
            response = f"{user} nie ma jeszcze żadnych korniszonów :)"
            return wait_find_input_and_send_keys(driver, 10, By.ID, "chat-text", response)
