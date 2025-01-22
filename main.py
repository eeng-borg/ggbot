from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import os
from selenium.common.exceptions import TimeoutException
from utils.utilities import waitFindInputAndSendKeys, waitFindAndReturn, waitFindAndClick, clearChat, filterBmp
from innitBot import initBot

from command_modules.binguj import binguj
from command_modules.bingusGpt import bingusGpt
from command_modules.zaczepiacz import zaczepiacz
from command_modules.help import help
from command_modules.korniszon_module.korniszon import korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from command import Command

# Set default encoding to UTF-8, to avoid UnicodeEncodeError
sys.stdout.reconfigure(encoding='utf-8')

# setup chrome profile, so it doesn't ask for logins
chrome_options = Options()
userPath = os.getenv('USER_PATH')
chrome_options.add_argument(f"user-data-dir={userPath}/AppData/Local/Google/Chrome/User Data")  # Path to your profile
chrome_options.add_argument("--profile-directory=Default")  # Default profile directory


# setup chrome driver
try:
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"Error initializing the Chrome driver: {e}")
    exit(1)

# initialize bot
initBot(driver)


# for testing purposes automatically send command
# WaitFindInputAndSendKeys(driver, 5, By.ID, "chat-text", "/binguj gf fdfd")
# time.sleep(1) # wait for the command to be sent

# initialize commands
binguj_command = Command(driver, 'binguj', "wpisz prompty na obrazek jaki chcesz wygenerować :)", True)
bingus_gpt_command = Command(driver, 'bingus', "zapytaj się bingusa o cokolwiek, może pomoże ;>", True)
korniszon_command = Command(driver, 'korniszon', "pokaż swojego korniszona, ocenimy uczciwie ;))", True)
ranking_command = Command(driver, 'ranking', "ranking dwudziestu najpotężniejszych korniszonów w kosmosie!!", False)
restart_command = Command(driver, 'restart', "gdyby się zawiesiło coś, gdzieś", False)
help_command = Command(driver, 'help', "pokazuje wszystkie komendy, ale skoro już tu jesteś to wiesz co robi :]", False)

leaderboard = Leaderboard()

# main loop for bot operations
while(True):
    # try to catch exceptions if command is found
    try:
            # check if binguj command is found and execute it

        if binguj_command.find_commands_and_nick():
            for prompt in binguj_command.find_commands_and_nick(): # prompt returns a list of tuples with prompt and nickname
                binguj(driver, prompt)  # Call Binguj function with the command as an argument
        
        # check if chatgpt command is found and execute it
        elif bingus_gpt_command.find_commands_and_nick():
            for prompt in bingus_gpt_command.find_commands_and_nick():
                bingusGpt(driver, prompt)
        
        elif korniszon_command.find_commands_and_nick():
            for korniszon_text in korniszon_command.find_commands_and_nick():
                korniszon(driver, korniszon_text, leaderboard)

        elif ranking_command.find_commands_and_nick():
            for ranking_text in ranking_command.find_commands_and_nick():
                # leaderboard = Leaderboard()
                leaderboard.load_leaderboard()
                leaderboard.display_leaderboard(driver)
            
        
        # elif makeZaczepka:
        #     zaczepiacz(driver, zaczepkaPrompt)

        #restart a bot
        elif restart_command.find_commands_and_nick():
            for restart_text in restart_command.find_commands_and_nick():
                waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", "Restartuje się <palacz>")
                initBot(driver)

        elif help_command.find_commands_and_nick():
            for command_list in help_command.find_commands_and_nick():
                Command.help(driver)
                clearChat(driver) # list of commands can trigger some commands


    except TimeoutException:
        print("Timeout occurred while executing function")
        driver.switch_to.window(driver.window_handles[0])
        safe_text = prompt if isinstance(prompt, str) else str(binguj_command.find_commands_and_nick())
        waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", f"Nie udało się wybingować {safe_text} ;(")
        continue

    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}, {e}")
        driver.switch_to.window(driver.window_handles[0])
        continue

    # input("Press Enter to exit...")
