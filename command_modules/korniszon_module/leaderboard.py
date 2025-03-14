from sql_database import Database
from utils.utilities import wait_find_input_and_send_keys
from utils.types import CommandData
import json
import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from typing import Dict, Optional
from werkzeug.exceptions import HTTPException


# korniszon leaderboard
class Leaderboard:


    leaderboard_file_name = "leaderboard_new.json"

    def __init__(self, database: Database, driver: Optional[webdriver.Chrome] = None, wait_find_input_and_send_keys=wait_find_input_and_send_keys):
        self.database = database
        self.leaderboard = []
        self.driver = driver
        self.leaderboard_is_displayed = False
        self.wait_find_input_and_send_keys = wait_find_input_and_send_keys
        # self.load_leaderboard()



    def load_leaderboard(self,  offset=0, limit=10, sort_by='score', order='DESC', whole=False):

        _leaderboard = []

        
        table = os.getenv('MAIN_TABLE_NAME')  # MAIN_TABLE_NAME=korniszons_test

        # Validate order parameter
        order = order.upper() if order.upper() in ['ASC', 'DESC'] else 'DESC'

        # Validate sort_by parameter - map frontend names to database columns
        valid_columns = {
            'score': 'score',
            'user': 'user',
            'input': 'input',
            'created': 'created',
            'position': 'position'
        }
        
        # Default to score if invalid column name provided
        sort_by = valid_columns.get(sort_by.lower(), 'score')
        
        query = f"""SELECT * 
                FROM {table}_with_position
                ORDER BY {sort_by} {order}, score DESC"""
                
        
        params = None
        
        if whole == False:
            query += " LIMIT %s OFFSET %s"
            params = (limit, offset)

        database = self.database.fetch(query, params, dictionary=True) or []
        
        for item in database:
            temp_item = item.copy()
            
            try:
                created_dt = item['created']
                if isinstance(created_dt, datetime):

                    # Convert datetime to Unix timestamp (seconds since epoch)
                    temp_item['created'] = created_dt.timestamp()

                else:

                    print(f"Warning: 'created' is not a datetime object, it's {type(created_dt)}")
                    # Try to parse it as datetime if it's a string
                    if isinstance(created_dt, str):

                        parsed_dt = datetime.strptime(created_dt, "%Y-%m-%d %H:%M:%S")
                        temp_item['created'] = parsed_dt.timestamp()
                    else:

                        temp_item['created'] = 0
                        
            except Exception as e:
                print(f"Error handling datetime: {e}, value: {item['created']}")
                temp_item['created'] = 0
            
            _leaderboard.append(temp_item)
        
        return _leaderboard
    


    def load_leaderboard_whole(self):
        table = os.getenv('MAIN_TABLE_NAME')
        query = f"""SELECT * 
                    FROM {table}_with_position"""
        
        database = self.database.fetch(query, dictionary=True) or []

        self.leaderboard = database
            



    def add_korniszon(self, command_data, score: float):

        korniszon_table = os.getenv('MAIN_TABLE_NAME')
        query = f"INSERT INTO {korniszon_table} (user, input, score, created) VALUES (%s, %s, %s, %s)"

        created = datetime.fromtimestamp(command_data.get('timestamp')).strftime("%Y-%m-%d %H:%M:%S")

        values = (command_data.get('user'), command_data.get('input'), score, created)

        self.database.commit(query, values)

        # self.leaderboard = sorted_leaderboard
    

    
    
    def get_position(self, korniszon_input):

        # Convert dict keys to a list and find index to determine it's position on leaderboard
        # new_korniszon returns leaderboard_sorted

        table = os.getenv('MAIN_TABLE_NAME')
        query = f"""
                SELECT position
                FROM {table}_with_position
                WHERE input COLLATE utf8mb4_bin = %s
                """

        position = self.database.fetch(query, (korniszon_input,), fetch_one=True)

        return position

        


    # get offset and limit arguments from command input
    def _get_range_from_input(self, data_input) -> Dict:

        # remove everything except numbers and spaces
        offset = 1
        limit = 10

        # remove everything exept for numbers and spaces, 
        numbers = "".join([char for char in data_input if char.isdigit() or char.isspace()])
        
        # then remove any spaces before or after, if there's a number and a word, then it will leave a space
        # and then it will count it as a second input after a split
        numbers_stripped = numbers.strip()
        input_list = numbers_stripped.split(" ")


        print(f"inputs: {input_list}")
        print(f"input_list: {len(input_list)}")

        try:
            # if only offset given
            if len(input_list) > 0:
                offset_input = int(input_list[0])

                # we later subract -1 from offset, so we don't want to trigger sql error 
                # which can't have items at -1 index 
                if offset_input > 0:
                    offset = int(input_list[0])
                    limit = 1 # assume we only want one position returned

                else:
                    response = f"Ranking zaczyna się od 1 <prosi>"
                    self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)


            # if both
            if len(input_list) > 1:
                limit = int(input_list[1])

        except ValueError:
            pass

        # subtract -1 so when asked for offset 5, we start from 5 and not 6
        return {"offset": offset - 1, "limit": limit}
    

    


    def _check_if_range_not_too_big(self, limit, max_range=30):

        if limit > max_range:

            response = f"Hola komboju <luzik> {limit} nie dostaniesz, masz 30."
            self.wait_find_input_and_send_keys(self.driver, 1, By.ID, "chat-text", response)
            time.sleep(1)
            print(f"limit: {limit}")

            # shorten the range to match the max_range, by decreasing the end index
            limit = max_range

        return limit




    def display_leaderboard(self, data_input, get_range_from_input=None):
        

        if self.leaderboard_is_displayed == False:

            self.leaderboard_is_displayed = True

            offset = 0
            limit = 10

            # if empty command
            if len(data_input) > 0: # input always return string, empty string acts like none
                # remove everything except numbers and spaces
                if get_range_from_input == None:
                    get_range_from_input = self._get_range_from_input
                    

                range_dict = get_range_from_input(data_input)
                offset = range_dict["offset"]
                limit = range_dict["limit"]

            
            # check if range not too big, to avoid spamming with 1k long ranking lists
            # if it is - subtract the end range value
            limit = self._check_if_range_not_too_big(limit)

                       
            # from index jest gdzieś -1 robiony sprawdź

            ranking_range = self.load_leaderboard(offset=offset, limit=limit)

            response = ''

            for ranking_position in ranking_range:

                position = ranking_position['position']
                input = ranking_position['input']
                user = ranking_position['user']
                score = ranking_position['score']


                response += f"{position}. {input} - {score}"

                if user is not None:
                    response += f" ({user})"
                
                response += "\n"


            self.wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
            self.leaderboard_is_displayed = False
            return response
        
        else:
            response = "Poczekaj aż pokażę cała listę <luzik>"
            self.wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)

            return ''
        




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
                f"Łacznie zdobytych punktów: {round(score_sum, 2)}\n"
                f"Średnia punktów: {round(score_average, 2)}\n"
                f"Ilość korniszonów: {quantity}\n"
                f"Top 3 korniszonów:\n"
            )
            response += "\n".join(best_tree)

            return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
            
        else:
            response = f"{user} nie ma jeszcze żadnych korniszonów :)"
            return wait_find_input_and_send_keys(self.driver, 10, By.ID, "chat-text", response)
