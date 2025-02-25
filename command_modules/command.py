from selenium.webdriver.common.by import By
from utils.utilities import filter_bmp, clear_chat, wait_find_input_and_send_keys
from utils.types import CommandData
from datetime import datetime
from selenium import webdriver
from typing import List
import time
from selenium.webdriver.remote.webelement import WebElement


class Command:

    # -- CLASS ATRIBUTES    
    command_type_list = [] # List of all commands and their descriptions, to use in help command 
    received_commands = [] # list of all commands extracted from messages

    # this flag is triggered after any command is found, so then we can run clear_chat() after the last command logic was executed
    is_any_command_found = False


    def __init__(self, driver: webdriver.Chrome, command_name: str, description: str):

        Command.driver = driver
        self.command_name = command_name
        self.description = description
        # List of last command uses in the chat before clearing it, just for temporary use

        # add command name and description to use it in /help
        Command.command_type_list.append({"command_name": command_name, "description": description})

    # get command name while initing
    def __str__(self):
        return str(self.command_name)

    @staticmethod
    def __commandXpath(command_name):

        xpath = ( #image generation command
        "//*[@class='ml__item-part-content' " # if command is in the active chat
        f"and contains(concat(' ',normalize-space(text()), ' '), ' /{command_name} ') "
        f"and starts-with(normalize-space(text()), '/{command_name}')]"
        )

        return xpath
    
    
    @staticmethod
    def __get_input_text(raw_command_element, command_name):
        input = raw_command_element.text.lstrip(f"/{command_name}")
        input = input.strip()  # remove whitespaces from the start and end of the text
        input = filter_bmp(input)  # Filter out unsupported characters from the text

        return input
    
    
    @staticmethod
    def __get_username(nickname_element):
        user_nickname = nickname_element.text
        user_nickname = user_nickname.replace(",", "") # theres a comma after a nickname ib ml__item-username text
        user_nickname = filter_bmp(user_nickname)

        return user_nickname
    
    @staticmethod
    def __make_data_dict(user_nickname, command_name, input):

        # Add command info to the dictionary
        command_data = {}
        
        command_data["user"] = user_nickname
        command_data["command"] = command_name
        command_data["input"] = input
        command_data['timestamp'] = int(time.time())

        time_data = {}

        time_data["hour"] = datetime.now().hour
        time_data["minute"] = datetime.now().minute
        time_data["day"] = datetime.now().day
        time_data["month"] = datetime.now().month
        time_data["year"] = datetime.now().year

        command_data["time"] = time_data

        return command_data
    

    # look for every command in the chat before clearing it, then put them in the list with all of their data (who posted, what type of command etc.)
    @staticmethod
    def get_commands_data(incoming_messages: List[WebElement]):

        Command.received_commands = [] # clear the list before every search, so it won't add up with old commands


        __user_nickname = ''

        for message in incoming_messages:          

            # if message elements contains user nickname element, it means that the other messages below, without it, belong to the same user
            nickname_element = message.find_elements(By.CLASS_NAME, "ml__item-username")


            if nickname_element:
                # Extract and clean the nickname so only string is left
                __user_nickname = Command.__get_username(nickname_element[0])

            # check for every command saved in type_list
            for command in Command.command_type_list:

                command_name = command['command_name']
                xpath = Command.__commandXpath(command_name)
                raw_command_element = message.find_elements(By.XPATH, f".{xpath}")  # Wait until the command is found and make a list of them

                # one of the command is found in this message
                if raw_command_element:

                    Command.is_any_command_found = True

                    # get input text from raw_command_element[0] and remove command name from it so only input text is left
                    input = Command.__get_input_text(raw_command_element[0], command_name)

                    # combine all collected data into a dict
                    command_data = Command.__make_data_dict(__user_nickname, command_name, input)
                    print(command_data)

                    Command.received_commands.append(command_data)
                    # print(f"Lista: {Command.received_commands}")

                    break # if command is found in this message, theres not point of checking for others, 
                            # so we skip to the next message


    # function to check if a specific command type is present in received_cmd list and make list of them
    @staticmethod
    def get_commands_by_type(command_type):

        searched_commands = []
        for command in Command.received_commands:
            if command['command'] == command_type:
                searched_commands.append(command)
        
        return searched_commands
            
    
    # display a list of all commands and their descriptions
    @staticmethod
    def help():
        for command in Command.command_type_list:
            response = f"/{command['command_name']} - {command['description']}"
            wait_find_input_and_send_keys(Command.driver, 1, By.ID, "chat-text", response)
