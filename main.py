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

# initialize bot and return tabs
tabs = initBot(driver)


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

        # checks if any commands are found
        binguj_commads_data = binguj_command.get_commands_data()

        if binguj_commads_data:
            for data in binguj_commads_data: # prompt returns a list of tuples with prompt and nickname
                binguj(driver, data["input"], tabs)  # Call Binguj function with the command as an argument
        

        bingus_gpt_commands_data = bingus_gpt_command.get_commands_data()

        if bingus_gpt_command.get_commands_data():
            for data in bingus_gpt_commands_data:
                bingusGpt(driver, data["input"], tabs)
        

        korniszon_commands_data = korniszon_command.get_commands_data()

        if korniszon_commands_data:
            for data in korniszon_commands_data:
                korniszon(driver, data, leaderboard)


        ranking_commands_data = ranking_command.get_commands_data()

        if ranking_commands_data:
            for data in ranking_commands_data:
                leaderboard.load_leaderboard()
                leaderboard.display_leaderboard(driver)


        #restart a bot
        restart_commands_data = restart_command.get_commands_data()

        if restart_commands_data:
            for data in restart_commands_data:
                waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", "Restartuje się <palacz>")
                initBot(driver)


        help_commands_data = help_command.get_commands_data()

        if help_commands_data:
            for data in help_commands_data:
                Command.help()
                clearChat(driver) # list of commands can trigger some commands


    except TimeoutException:
        print("Timeout occurred while executing function")
        driver.switch_to.window(driver.window_handles[0])
        waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", "Coś sie nie udało ;(")
        continue

    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}, {e}")
        driver.switch_to.window(driver.window_handles[0])
        continue

