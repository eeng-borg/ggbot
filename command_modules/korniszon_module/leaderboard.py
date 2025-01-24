from utils.utilities import waitFindInputAndSendKeys, waitFindAndReturn, waitFindAndClick, clearChat, filterBmp
import json
import os
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
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x.get('score', 0), reverse=True)        # print(sorted_leaderboard)
        
        # Save to a JSON file
        with open(self.leaderboard_file_name, 'w', encoding='utf-8') as f:
            json.dump(sorted_leaderboard, f, indent=4 )

        print("Save to a JSON file:  {self.leaderboard}")
        
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
                waitFindInputAndSendKeys(driver, 10, By.ID, "chat-text", response)
                index +=1

                if index > 10:
                    break
            else:
                response = "Nic tu nie ma, zrób najpierw jakieś korniszony może :)"
                waitFindInputAndSendKeys(driver, 10, By.ID, "chat-text", response)
        
        clearChat(driver)
