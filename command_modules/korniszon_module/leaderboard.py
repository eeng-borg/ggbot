from http.client import responses

from utils.utilities import wait_find_input_and_send_keys
from utils.types import CommandData
import json
import os
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from typing import Dict, Optional


# korniszon leaderboard
class Leaderboard:

    leaderboard_file_name = "leaderboard_new.json"

    def __init__(self, driver: Optional[webdriver.Chrome] = None, wait_find_input_and_send_keys=wait_find_input_and_send_keys):
        self.leaderboard = []
        self.driver = driver
        self.leaderboard_is_displayed = False
        self.wait_find_input_and_send_keys = wait_find_input_and_send_keys


    def load_leaderboard(self):

        # check if file exists already, if not made one
        if not os.path.exists(self.leaderboard_file_name):
            print("JSON nie istnije!!")

            # Save dict to a JSON file if it doesn't exist
            with open(self.leaderboard_file_name, 'w', encoding='utf-8') as f:
                json.dump(self.leaderboard, f, indent=4)


        # load dict from a JSON file        
        with open(self.leaderboard_file_name, 'r', encoding='utf-8') as f:
                self.leaderboard = json.load(f)




    def add_korniszon(self, command_data: CommandData, score: float):

        new_korniszon = {}

        # add score to new_korniszon data and remove command key
        for data_key, data_value in command_data.items():
            new_korniszon[data_key] = data_value

        # every command here is /korniszon, so we don't need it 
        del new_korniszon['command']
        new_korniszon["score"] = score

        # add new result
        self.leaderboard.append(new_korniszon)

        # print(f"add new result:  {self.leaderboard}")

        # sort
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x.get('score', 0), reverse=True) # print(sorted_leaderboard)
        
        # add updated position
        for index, korniszon in enumerate(sorted_leaderboard):
            korniszon["position"] = index + 1


        # Save to a JSON file
        with open(self.leaderboard_file_name, 'w', encoding='utf-8') as f:
            # print(f"Zapisuje: {sorted_leaderboard}")
            json.dump(sorted_leaderboard, f, indent=4)

        
        self.leaderboard = sorted_leaderboard
    

    
    
    def get_position(self, korniszon_text) -> int | None:

        # Convert dict keys to a list and find index to determine it's position on leaderboard
        # new_korniszon returns leaderboard_sorted

        for item in self.leaderboard:

            if item.get("input") == korniszon_text:
                position = self.leaderboard.index(item) + 1
                print(f"position: {position}")

                return position
        


    
    # def find_by_name(self, korniszon_text):
    #     self.leaderboard
    @staticmethod
    def _get_range_from_input(data_input) -> Dict:
        # remove everything except numbers and spaces
        from_index = 0
        to_index = 10

        # remove everything exept for numbers and spaces, 
        numbers = "".join([char for char in data_input if char.isdigit() or char.isspace()])
        
        # then remove any spaces before or after, if there's a number and a word, then it will leave a space
        # and then it will count it as a second input after a split
        numbers_stripped = numbers.strip()
        input_list = numbers_stripped.split(" ")


        print(f"inputs: {input_list}")
        print(f"input_list: {len(input_list)}")

        try:
            if len(input_list) >= 2:
                from_index = int(input_list[0]) - 1
                to_index = int(input_list[1])

            elif len(input_list) == 1:
                to_index = int(input_list[0])

        except ValueError:
            return {"from_index": from_index, "to_index": to_index}


        return {"from_index": from_index, "to_index": to_index}
    

    


    def _check_if_range_is_too_big(self, from_index, to_index, max_range=30):
        


        index_range = to_index - from_index # 120 - 30 = 90
        print(f"Kalkuluj: {index_range} = {to_index} - {from_index}")

        if index_range > max_range:

            response = f"Hola komboju <luzik> {index_range} nie dostaniesz, masz 30."
            self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)
            time.sleep(1)
            print(f"to_index: {to_index}")

            # shorten the range to match the max_range, by decreasing the end index
            to_index = to_index - (index_range - max_range)

        return to_index




    def display_leaderboard(self, data_input, get_range_from_input=_get_range_from_input):
        

        if self.leaderboard_is_displayed == False:
            self.leaderboard_is_displayed = True

            from_index = 0
            to_index = 10

            if len(data_input) > 0: # input always return string, empty string acts like none
                # remove everything except numbers and spaces
                range_dict = get_range_from_input(data_input)
                from_index = range_dict["from_index"]
                to_index = range_dict["to_index"]

            
            # check if range not too big, to avoid spamming with 1k long ranking lists
            # if it is - subtract the end range value
            to_index = self._check_if_range_is_too_big(from_index, to_index)

            responses = []


            if len(self.leaderboard) > 0:
                for korniszon in self.leaderboard[from_index : to_index]:

                    input = korniszon.get("input")
                    score = korniszon.get("score")
                    user = korniszon.get("user")
                    position = korniszon.get("position")

                    response = f"{position}. {input} - {score}"

                    # not all korniszons have users, so I want add them only if it's not None, otherwise don't add anything
                    if user:
                        response += f" ({user})"

                    responses.append(response) # for testing

                    self.wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)


            else:
                response = "Nic tu nie ma, zrób najpierw jakieś korniszony może :)"
                self.wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)


            self.leaderboard_is_displayed = False
            return responses
        
        
        else:
            response = "Poczekaj aż pokażę całą listę <luzik>"
            self.wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)

            return []
        




    # -------------------------

    # user stats

    def __get_user_score_sum(self, user) -> float:

        score_sum = 0

        for korniszon in self.leaderboard:
            if korniszon.get("user") == user:
                score = korniszon.get("score")
                score_sum += score

        return score_sum
    


    
    def __get_user_average_score(self, user) -> float:

        score_sum = self.__get_user_score_sum(user)
        score_average = 0
        index = 0

        for korniszon in self.leaderboard:
            if korniszon.get("user") == user:
                index += 1

        score_average = score_sum / index

        return score_average
    



    def ___get_user_korniszons(self, user, how_many=float('inf')) -> list[str]: # get infinite float and convert it to int and assign it if how_many is not given
        
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
    def display_user_stats(self, data: CommandData):
        
        user = ''

        if data.get('input') == '':
            user = data.get('user')
        
        else:
            user = data.get('input')

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

            return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
            
        else:
            response = f"{user} nie ma jeszcze żadnych korniszonów :)"
            return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
