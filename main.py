from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import io
import os
import platform
from dotenv import load_dotenv, find_dotenv
import asyncio
from selenium.common.exceptions import TimeoutException
from utils.utilities import wait_find_input_and_send_keys, clear_chat
from innit_bot import innit_bot
import logging as Log

import traceback
from datetime import datetime


from command_modules.binguj import binguj
from command_modules.bingus_gpt import bingus_gpt
from command_modules.korniszon_module.korniszon import korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from command_modules.korniszon_module.best_korniszon_by_day import best_korniszon_by_day 
from command_modules.korniszon_module.random_korniszon import SpamKorniszon
from command_modules.command import Command



# Set default encoding to UTF-8, to avoid UnicodeEncodeError
# sys.stdout.reconfigure(encoding='utf-8')
# setup chrome profile, so it doesn't ask for logins

print("Running")

load_dotenv(find_dotenv())

# create crash logs file
def log_exception(exc_type, exc_value, exc_traceback):
    with open("crash-log.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}\n\n") # when error happend
        f.write("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))        
        f.write("\n" + "="*80 + "\n")  # separator for clarity

sys.excepthook = log_exception


# driver
def create_driver() -> webdriver.Chrome:

    print("Driver created")
    chrome_options = Options()
    

    # Prevent Chrome from closing due to multiple instances
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-application-cache")

    # Enable headless mode for production
    # if hasattr(sys, "_MEIPASS"):
    os_type = platform.system()

    if os_type == "Linux":
        chrome_options.add_argument("--headless=new")  # Run Chrome in headless mode
        chrome_options.add_argument("--start-maximized") # so it looks more human-like
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended in headless mode)
        chrome_options.add_argument("--no-sandbox")  # Disable sandboxing for headless mode (some environments need this)
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
        chrome_options.add_argument("--window-size=800x600")  # Ensure proper rendering

    
    # Avoid Chrome crash by disabling shared memory
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        if os_type == "Linux":
            print("Running on Linux server")
            service = Service("/usr/local/bin/chromedriver")
            user_data_dir = os.getenv('PROD_PROFILE') # production

        elif os_type == "Windows":
            print("Running on Windows local")
            service = Service("./chromedriver.exe") #change to exe for windows
            user_data_dir = os.getenv('DEV_PROFILE') # development         

        
        # Use a different user data directory for each instance
        profile_path = os.getenv('PROFILE_PATH')
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        chrome_options.add_argument(f"--profile-directory={user_data_dir}")  # Default profile directory

        
        # create a driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

    except Exception as e:
        print(f"Error initializing the Chrome driver: {e}")
        exit(1)

    return driver


# for testing purposes, if there argument "test", start chat with me (testing). Otherwise start chat with Komfa




# initialize bot and return tabs
driver = create_driver()
tabs = innit_bot(driver)

print("Bot initiaindi completed")

# for testing purposes automatically send command
# wait_find_input_and_send_keys(driver, 5, By.ID, "chat-text", "/binguj gf fdfd")
# time.sleep(1) # wait for the command to be sent

# initialize commands
binguj_command = Command(driver, 'binguj', "wpisz prompty na obrazek jaki chcesz wygenerować :)")
bingus_gpt_command = Command(driver, 'bingus', "zapytaj się bingusa o cokolwiek, może pomoże ;>")
korniszon_command = Command(driver, 'korniszon', "pokaż swojego korniszona, ocenimy uczciwie ;))")
spam_command = Command(driver, 'spam', "co ile sekund ma spamować korniszonami <chatownik>") 
torniszon_command = Command(driver, 'topniszon', "najlepszy korniszon z dziś <okularnik>")
ranking_command = Command(driver, 'ranking', "ranking najpotężniejszych korniszonów w kosmosie!! Podaj 1-2 numery, aby określić zakres.")
user_korniszon_stats_command = Command(driver, 'staty', "korniszonistyki zawodnika <paker>")
restart_command = Command(driver, 'restart', "gdyby się zawiesiło coś, gdzieś")
help_command = Command(driver, 'help', "pokazuje wszystkie komendy, ale skoro już tu jesteś to wiesz co robi :]")

leaderboard = Leaderboard()
leaderboard.load_leaderboard()
spam_korniszon = SpamKorniszon()

# main loop for bot operations
while(True):

    # try to catch exceptions if command is found
    try:
        # check chat for commands and return data of them
        binguj_commads_data = binguj_command.get_commands_data()
        korniszon_commands_data = korniszon_command.get_commands_data()
        spam_commands_data = spam_command.get_commands_data()
        torniszon_commands_data = torniszon_command.get_commands_data()
        ranking_commands_data = ranking_command.get_commands_data()
        user_stats_data = user_korniszon_stats_command.get_commands_data()
        restart_commands_data = restart_command.get_commands_data()
        help_commands_data = help_command.get_commands_data()
        # bingus_gpt_commands_data = bingus_gpt_command.get_commands_data()

        # functions not called by a command
        spam_korniszon.spamming(driver, leaderboard)


        # functions called with a command
        if Command.is_any_command_found:
            clear_chat(driver) # clear chat before exec logic, so we can still get commands which were posted during this

            if binguj_commads_data:
                for data in binguj_commads_data: # prompt returns a list of tuples with prompt and nickname
                    binguj(driver, str(data["input"]), tabs)  # Call Binguj function with the command as an argument

            # if bingus_gpt_commands_data:
            #     for data in bingus_gpt_commands_data:
            #         bingus_gpt(driver, data, tabs)    

            if korniszon_commands_data:
                for data in korniszon_commands_data:
                    korniszon(driver, data, leaderboard)

            if spam_commands_data:
                for data in spam_commands_data:

                    # if '-l' in data['input'] and data['user'] == 'Ing': # check for -l flag for limit and if user is admin
                    #     input_data = data['input'].replace(' -l ','')
                    #     SpamKorniszon.spam_limit = int(input_data)
                    #     response = f"Limit ustawiony na {SpamKorniszon.spam_limit} szefie <faja>"
                    #     wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", response)
                    # else:
                    spam_korniszon.set_spamming_time(driver, data)

            if torniszon_commands_data:
                for data in torniszon_commands_data:
                    best_korniszon_by_day(driver, data, leaderboard)

            if ranking_commands_data:
                for data in ranking_commands_data:
                    # leaderboard.load_leaderboard()
                    leaderboard.display_leaderboard(driver, data["input"])

            if user_stats_data:
                for data in user_stats_data:
                    # leaderboard.load_leaderboard()
                    leaderboard.display_user_stats(driver, data)

            if restart_commands_data:
                for data in restart_commands_data:
                    wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", "Restartuje się <palacz>")
                    innit_bot(driver)        

            if help_commands_data:
                for data in help_commands_data:
                    Command.help()
        
            # after we checked the chat for commands, clear it from the messages so we won't use them again.
            Command.is_any_command_found = False


    except TimeoutException:
        print("Timeout occurred while executing function")
        driver.save_screenshot("debug_screenshot2.png")

        driver.switch_to.window(tabs["main tab"])
        wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", "Coś sie nie udało ;(")
        continue    

    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}, {e}")
        driver.switch_to.window(tabs["main tab"])
        continue
    