from selenium.webdriver.common.by import By
from utils.utilities import filterBmp, clearChat, waitFindInputAndSendKeys

class Command:

    # List of all commands and their descriptions, to use in help command
    command_type_list = []
    driver = None
    

    def __init__(self, driver, command_name, description, text_after_command : bool):

        Command.driver = driver
        self.command_name = command_name
        self.description = description
        self.text_after_command = text_after_command
        self.commands = {}

        Command.command_type_list.append(f"/{command_name} - {description}")


    def __commandXpath(self):
    
        xpath = ""

        if(self.text_after_command == True):

            xpath = ( #image generation command
            "//*[@class='ml__item-part-content' " #check if command is in the active chat
            f"and starts-with(normalize-space(text()), '/{self.command_name} ') " #check if command starts with '/binguj '
            f"and string-length(normalize-space(text())) > string-length('/{self.command_name} ')]" #check if command is not empty after '/binguj '
            )

        # for commands like 'restart' which don't need additional instructions 
        else:
            xpath = (
            "//*[@class='ml__item-part-content' "
            f"and normalize-space(text())='/{self.command_name}']"
            )
        
        # make list of all command names and it description to use it in /help
        

        return xpath
    

    # Find the nickname of the user who sent the command. If someone wrote multiple messages in a row, 
    # find their first message to get the element with the nickname.
    def find_commands_and_nick(self):

        self.commands = {}
        # Only incoming messages, so the bot can ignore itself (outgoing messages)
        incoming_messages = self.driver.find_elements(By.CLASS_NAME, "ml__item--incoming")
        is_command_found = False

        if incoming_messages:
            command_text = ""
            user_nickname = ""

            for message in reversed(incoming_messages):
                # xpath to find specific commands in the chat
                xpath = self.__commandXpath()
                raw_command_elements = message.find_elements(By.XPATH, f".{xpath}")  # Wait until the command is found and make a list of them

                # Check if the user has sent a GPT command and turn on a switch to look for the user's nickname
                if raw_command_elements:
                    print(f"Message: {raw_command_elements[0].text}")
                    command_text = raw_command_elements[0].text.replace(f"/{self.command_name} ", "")  
                    command_text = filterBmp(command_text)  # Filter out unsupported characters from the text

                    is_command_found = True

                # Look for the nickname only if the user sent a command
                if is_command_found:
                    nickname_elements = message.find_elements(By.CLASS_NAME, "ml__item-username")
                    print(f"Nick found: {len(nickname_elements)}")

                    if nickname_elements:
                        print(f"Nick: {nickname_elements[0].text}")

                        # Extract and clean the nickname
                        user_nickname = nickname_elements[0].text
                        user_nickname = filterBmp(user_nickname)

                        # Add the command and nickname to the dictionary
                        self.commands[command_text] = user_nickname
                        print(self.commands)

                        # Reset the command-found flag for the next iteration
                        is_command_found = False

            
        return self.commands
    
    
    # display a list of all commands and their descriptions
    @staticmethod
    def help():
        for line in Command.command_type_list:
            waitFindInputAndSendKeys(Command.driver, 1, By.ID, "chat-text", line)
    
    
    

