from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import io
import os
from dotenv import load_dotenv
import asyncio
from selenium.common.exceptions import TimeoutException
from utils.utilities import wait_find_input_and_send_keys, clear_chat
from innit_bot import innit_bot
import logging as Log


from command_modules.binguj import binguj
from command_modules.bingus_gpt import bingus_gpt
from command_modules.korniszon_module.korniszon import korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from command_modules.korniszon_module.best_korniszon_by_day import best_korniszon_by_day 
from command_modules.korniszon_module.random_korniszon import post_random_korniszon
from command_modules.command import Command



# Set default encoding to UTF-8, to avoid UnicodeEncodeError
# sys.stdout.reconfigure(encoding='utf-8')
# setup chrome profile, so it doesn't ask for logins


load_dotenv()


def create_driver(user_data_dir) -> webdriver.Chrome:

    chrome_options = Options()

    # Use a different user data directory for each instance
    profile_path = os.getenv('PROFILE_PATH')
    chrome_options.add_argument(f"--user-data-dir={profile_path}")
    chrome_options.add_argument(f"--profile-directory={user_data_dir}")  # Default profile directory

    # Enable headless mode for production
    if hasattr(sys, "_MEIPASS"):
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended in headless mode)
        chrome_options.add_argument("--no-sandbox")  # Disable sandboxing for headless mode (some environments need this)

    
    # Avoid Chrome crash by disabling shared memory
    chrome_options.add_argument("--disable-dev-shm-usage")


    # setup chrome driver
    try:
        service = Service(executable_path='chromedriver.exe')
        
        driver = webdriver.Chrome(service=service, options=chrome_options)

    except Exception as e:
        print(f"Error initializing the Chrome driver: {e}")
        exit(1)


    return driver


# get a diffrent chrome profile and gg chat depending if run it on exe or vscode
if hasattr(sys, "_MEIPASS"):
    # Running as an EXE
    profile = os.getenv('PROD_PROFILE') # production
    chat = 'Komfa'

    print("Running as a standalone EXE")

else:
    # Running in normal Python (VS Code, terminal, etc.)
    profile = os.getenv('DEV_PROFILE') # development
    test_chat = os.getenv('TEST_CHAT')

    chat = test_chat # test chat
    print("Running in a normal Python environment")


driver = create_driver(profile)


# print(f"user-data-dir={default_profile_path}")

# initialize bot and return tabs
tabs = innit_bot(driver, chat)

# for testing purposes automatically send command
# wait_find_input_and_send_keys(driver, 5, By.ID, "chat-text", "/binguj gf fdfd")
# time.sleep(1) # wait for the command to be sent

# initialize commands
binguj_command = Command(driver, 'binguj', "wpisz prompty na obrazek jaki chcesz wygenerować :)")
bingus_gpt_command = Command(driver, 'bingus', "zapytaj się bingusa o cokolwiek, może pomoże ;>")
korniszon_command = Command(driver, 'korniszon', "pokaż swojego korniszona, ocenimy uczciwie ;))")
torniszon_command = Command(driver, 'topniszon', "najlepszy korniszon z dziś <okularnik>")
ranking_command = Command(driver, 'ranking', "ranking najpotężniejszych korniszonów w kosmosie!! Podaj 1-2 numery, aby określić zakres.")
user_korniszon_stats_command = Command(driver, 'staty', "korniszonistyki zawodnika <paker>")
restart_command = Command(driver, 'restart', "gdyby się zawiesiło coś, gdzieś")
help_command = Command(driver, 'help', "pokazuje wszystkie komendy, ale skoro już tu jesteś to wiesz co robi :]")

leaderboard = Leaderboard()
leaderboard.load_leaderboard()


# main loop for bot operations
while(True):

    # try to catch exceptions if command is found
    try:
        # asyncio.run(post_random_korniszon(driver, leaderboard))

        # checks if any commands are found
        binguj_commads_data = binguj_command.get_commands_data()

        if binguj_commads_data:
            for data in binguj_commads_data: # prompt returns a list of tuples with prompt and nickname
                binguj(driver, str(data["input"]), tabs)  # Call Binguj function with the command as an argument
        

        bingus_gpt_commands_data = bingus_gpt_command.get_commands_data()

        if bingus_gpt_commands_data:
            for data in bingus_gpt_commands_data:
                bingus_gpt(driver, data, tabs)
        

        korniszon_commands_data = korniszon_command.get_commands_data()

        if korniszon_commands_data:
            for data in korniszon_commands_data:
                korniszon(driver, data, leaderboard)

                
        torniszon_commands_data = torniszon_command.get_commands_data()

        if torniszon_commands_data:
            for data in torniszon_commands_data:
                best_korniszon_by_day(driver, data, leaderboard)


        ranking_commands_data = ranking_command.get_commands_data()

        if ranking_commands_data:
            for data in ranking_commands_data:
                leaderboard.load_leaderboard()
                leaderboard.display_leaderboard(driver, data["input"])


        # user_korniszon_stats_command
        user_stats_data = user_korniszon_stats_command.get_commands_data()

        if user_stats_data:
            for data in user_stats_data:
                leaderboard.load_leaderboard()
                leaderboard.display_user_stats(driver, data)
                

        #restart a bot
        restart_commands_data = restart_command.get_commands_data()

        if restart_commands_data:
            for data in restart_commands_data:
                wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", "Restartuje się <palacz>")
                innit_bot(driver, chat)


        help_commands_data = help_command.get_commands_data()

        if help_commands_data:
            for data in help_commands_data:
                Command.help()
                clear_chat(driver) # list of commands can trigger some commands


    except TimeoutException:
        print("Timeout occurred while executing function")
        driver.switch_to.window(tabs["main tab"])
        wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", "Coś sie nie udało ;(")
        continue    

    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}, {e}")
        driver.switch_to.window(tabs["main tab"])
        continue
