from utils.utilities import waitFindInputAndSendKeys, waitFindAndReturn, waitFindAndClick, clearChat, filterBmp
import json
import os
from selenium.webdriver.common.by import By


# korniszon leaderboard
class Leaderboard:

    leaderboard_file_name = "leaderboard.json"
    leaderboard = {}

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


    def new_korniszon(self, korniszon_text, score):

        # add new result
        self.leaderboard[korniszon_text] = score
        # print(f"add new result:  {self.leaderboard}")

        # sort
        leaderboard_sorted = dict(sorted(self.leaderboard.items(), key=lambda item: item[1], reverse=True))
        # print(leaderboard_sorted)
        
        # Save to a JSON file
        with open(self.leaderboard_file_name, 'w', encoding='utf-8') as f:
            json.dump(leaderboard_sorted, f, indent=4 )

        print("Save to a JSON file:  {self.leaderboard}")
        
        self.leaderboard = leaderboard_sorted
    
    
    def get_position(self, korniszon_text):

        # Convert dict keys to a list and find index to determine it's position on leaderboard
        # new_korniszon returns leaderboard_sorted
        position = list(self.leaderboard.keys()).index(korniszon_text) + 1
        print(f"position: {position}")

        return position
    
    # def find_by_name(self, korniszon_text):
    #     self.leaderboard

    def display_leaderboard(self, driver):
        index = 1
        
        for korniszon, score in self.leaderboard.items():

            if len(self.leaderboard) > 0:
                response = f"{index}. {korniszon} - {score}"
                waitFindInputAndSendKeys(driver, 10, By.ID, "chat-text", response)
                index +=1

                if index > 10:
                    break
            else:
                response = "Nic tu nie ma, zrób najpierw jakieś korniszony może :)"
                waitFindInputAndSendKeys(driver, 10, By.ID, "chat-text", response)
        
        clearChat(driver)
