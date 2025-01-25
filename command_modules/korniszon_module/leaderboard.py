from utils.utilities import wait_find_input_and_send_keys, wait_find_and_return, wait_find_and_click, clear_chat, filter_bmp
import json
import os
import math
from selenium.webdriver.common.by import By
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
                print(f"wczytana: {self.leaderboard}")

        except json.JSONDecodeError:
            print("Błąd JSON! Resetuję leaderboard.")
            # self.leaderboard = {}


    def add_korniszon(self, korniszon_data, score):

        # add score to new_korniszon data and remove command type
        new_korniszon = korniszon_data
        new_korniszon["score"] = score
        del new_korniszon["command"]

        # add new result
        self.leaderboard.append(new_korniszon)


        # print(f"add new result:  {self.leaderboard}")

        # sort
        print(f"Leaderboard przed sortowaniem: {self.leaderboard}")
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x.get('score', 0), reverse=True) # print(sorted_leaderboard)
        
        # Save to a JSON file
        with open(self.leaderboard_file_name, 'w', encoding='utf-8') as f:
            print(f"Zapisuje: {sorted_leaderboard}")
            json.dump(sorted_leaderboard, f, indent=4 )

        print(f"Save to a JSON file:  {self.leaderboard}")
        
        self.leaderboard = sorted_leaderboard
    
    
    def get_position(self, korniszon_text):

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

    def display_leaderboard(self, driver):
        index = 1
        
        for korniszon in self.leaderboard:
            input = korniszon.get("input")
            score = korniszon.get("score")

            log.info(f"Korniszon: {input}, score: {score}")
            if len(self.leaderboard) > 0:
                response = f"{index}. {input} - {score}"
                wait_find_input_and_send_keys(driver, 10, By.ID, "chat-text", response)
                index +=1

                if index > 10:
                    break
            else:
                response = "Nic tu nie ma, zrób najpierw jakieś korniszony może :)"
                wait_find_input_and_send_keys(driver, 10, By.ID, "chat-text", response)
        
        clear_chat(driver)

    # -------------------------

    # user stats

    def __get_user_score_sum(self, user):

        score_sum = 0

        for korniszon in self.leaderboard:
            if korniszon.get("user") == user:
                score = korniszon.get("score")
                score_sum += score

        return score_sum
    
    
    def __get_user_average_score(self, user):

        score_sum = self.__get_user_score_sum(user)
        score_average = 0
        index = 0

        for korniszon in self.leaderboard:
            if korniszon.get("user") == user:
                index += 1

        score_average = score_sum / index

        return score_average
    

    def ___get_user_korniszons(self, user: str, how_many: int = float('inf')) -> list: # infinite if how_many is not provided
        
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
    def display_user_stats(self, driver, user):
        
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
