from selenium.webdriver.common.by import By
from utils.utilities import filter_bmp, clear_chat, wait_find_input_and_send_keys
from utils.types import CommandData
from datetime import datetime
from selenium import webdriver
from typing import List


class Command:

    # -- CLASS ATRIBUTES 
    # List of all commands and their descriptions, to use in help command
    command_type_list = []

    # this flag is triggered after any command is found, so then we can run clear_chat() after the last command logic was executed
    is_any_command_found = False


    def __init__(self, driver: webdriver.Chrome, command_name: str, description: str):

        Command.driver = driver
        self.command_name = command_name
        self.description = description
        # List of last command uses in the chat before clearing it, just for temporary use

        # add command name and description to use it in /help
        Command.command_type_list.append(f"/{command_name} - {description}")


    def __commandXpath(self):

        xpath = ( #image generation command
        "//*[@class='ml__item-part-content' " # if command is in the active chat
        f"and contains(concat(' ',normalize-space(text()), ' '), ' /{self.command_name} ') "
        f"and starts-with(normalize-space(text()), '/{self.command_name}')]"
        )

        return xpath
    
    # # WIP - not implemented
    # # Find the nickname of the user who sent the command. If someone wrote multiple messages in a row, 
    # # find their first message to get the element with the nickname.
    # def get_command_elements(self):

    #     # Only incoming messages, so the bot can ignore itself (outgoing messages)
    #     incoming_messages = self.driver.find_elements(By.CLASS_NAME, "ml__item--incoming")

    #     command_elements = []

    #     if incoming_messages:
    #             for message in reversed(incoming_messages):
    #                 # print(f"Znaleziono: {len(incoming_messages)} wiadomości")
    #                 # xpath to find specific commands in the chat
    #                 xpath = self.__commandXpath()
    #                 raw_command_element = message.find_elements(By.XPATH, f".{xpath}")  # Wait until the command is found and make a list of them 

    #                 if raw_command_element:
    #                     command_elements.append(message)

    #             return command_elements

    
    def __get_input(self, raw_command_element):
        input = raw_command_element.text.lstrip(f"/{self.command_name}")
        input = input.strip()  # remove whitespaces from the start and end of the text
        input = filter_bmp(input)  # Filter out unsupported characters from the text

        return input
    
    # if user makes several commands at the same time, function will only catch
    def get_commands_data(self) -> List[CommandData]:

        received_commands = [] # list of all commands found in the chat before clearing it
        command_data = {} # data of a single command

        # Only incoming messages, so the bot can ignore itself (outgoing messages)
        incoming_messages = self.driver.find_elements(By.CLASS_NAME, "ml__item--incoming")
        is_command_found = False

        if incoming_messages:

            input = ""
            user_nickname = ""
            time = {}

            for message in reversed(incoming_messages):

                # print(f"Znaleziono: {len(incoming_messages)} wiadomości")
                # xpath to find specific commands in the chat
                xpath = self.__commandXpath()
                raw_command_element = message.find_elements(By.XPATH, f".{xpath}")  # Wait until the command is found and make a list of them

                # Check if the user has sent a command and turn on a switch to look for the user's nickname
                if raw_command_element:
                    print(f"Message: {raw_command_element[0].text}, remove: {self.command_name}")                

                    input = self.__get_input(raw_command_element[0])
                    is_command_found = True

                # when the command message is found, contionue iterating up trough incoming messages until you get the one
                # that contains the username
                if is_command_found:

                    Command.is_any_command_found = True
                    
                    nickname_elements = message.find_elements(By.CLASS_NAME, "ml__item-username")
                    print(f"Nick found: {len(nickname_elements)}")

                    if nickname_elements:
                        print(f"Nick: {nickname_elements[0].text}")

                        # Extract and clean the nickname
                        user_nickname = nickname_elements[0].text
                        user_nickname = user_nickname.replace(",", "") # theres a comma after a nickname ib ml__item-username text
                        user_nickname = filter_bmp(user_nickname)


                        # Add command info to the dictionary
                        command_data["user"] = user_nickname
                        command_data["command"] = self.command_name
                        command_data["input"] = input

                        time["hour"] = datetime.now().hour
                        time["minute"] = datetime.now().minute
                        time["day"] = datetime.now().day
                        time["month"] = datetime.now().month
                        time["year"] = datetime.now().year

                        command_data["time"] = time

                        received_commands.append(command_data)
                        print(command_data)

                        # Reset the command-found flag for the next iteration
                        is_command_found = False
                

        # it should return a list of dictionaries containing all information about the command - input, nickname, date    
        return received_commands
    
    
    # display a list of all commands and their descriptions
    @staticmethod
    def help():
        for line in Command.command_type_list:
            wait_find_input_and_send_keys(Command.driver, 1, By.ID, "chat-text", line)
