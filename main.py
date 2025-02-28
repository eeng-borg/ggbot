from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import os
import platform
import threading
from dotenv import load_dotenv, find_dotenv
from selenium.common.exceptions import TimeoutException
from utils.utilities import wait_find_input_and_send_keys, clear_chat
from innit_bot import innit_bot


import traceback
from datetime import datetime


from command_modules.binguj import binguj
# from command_modules.bingus_gpt import bingus_gpt
from command_modules.korniszon_module.korniszon import Korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from command_modules.korniszon_module.topniszon import Topniszon
from command_modules.korniszon_module.random_korniszon import SpamKorniszon
from command_modules.command import Command

from users import Cooldown



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
def __create_driver() -> webdriver.Chrome:

    print("Driver created")
    chrome_options = Options()
    

    # Prevent Chrome from closing due to multiple instances
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-application-cache")

    # Enable headless mode for production
    # if hasattr(sys, "_MEIPASS"):
    os_type = platform.system()


    if os_type == "Linux":

        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        # chrome_options.add_argument("--start-maximized") # so it looks more human-like
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended in headless mode)
        chrome_options.add_argument("--no-sandbox")  # Disable sandboxing for headless mode (some environments need this)
        chrome_options.add_argument("--disable-dev-shm-usage") # Avoid Chrome crash by disabling shared memory
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
        # chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v=1")
        chrome_options.add_argument("--window-size=800x600")  # Ensure proper rendering
    
    

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


# initialize bot and return tabs
driver = __create_driver()
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
topniszon_command = Command(driver, 'topniszon', "najlepszy korniszon z dziś <okularnik>")
ranking_command = Command(driver, 'ranking', "ranking najpotężniejszych korniszonów w kosmosie!! Podaj 1-2 numery, aby określić zakres.")
staty_command = Command(driver, 'staty', "korniszonistyki zawodnika <paker>")
# restart_command = Command(driver, 'restart', "gdyby się zawiesiło coś, gdzieś")
strona_command = Command(driver, 'strona', "gg platforma z różnymi ciekawymi rzeczami <chatownik>")
help_command = Command(driver, 'help', "pokazuje wszystkie komendy, ale skoro już tu jesteś to wiesz co robi :]")


leaderboard = Leaderboard(driver)
korniszon = Korniszon(driver, leaderboard)
leaderboard.load_leaderboard()
spam_korniszon = SpamKorniszon(driver, leaderboard)
topniszon = Topniszon(driver)



# main loop for bot operations
while(True):

    # try to catch exceptions if command is found
    try:
        # Only incoming messages, so the bot can ignore itself (outgoing messages)
        incoming_messages = driver.find_elements(By.CLASS_NAME, "ml__item--incoming")

        
        if incoming_messages:

            # search for commands in messages and return data of them
            Command.get_commands_data(incoming_messages)

            
            # functions called with a command
            if Command.is_any_command_found:

                clear_chat(driver) # clear chat before exec logic, so we can still get commands which were posted during this
                
                binguj_commads_data = Command.get_commands_by_type(str(binguj_command))

                if binguj_commads_data:
                    for data in binguj_commads_data:
                        binguj(driver, str(data["input"]), tabs)


                # if bingus_gpt_commands_data:
                #     for data in bingus_gpt_commands_data:
                #         bingus_gpt(driver, data, tabs)


                #   ---Korniszon--- 
                korniszon_commands_data = Command.get_commands_by_type(str(korniszon_command))
                
                if korniszon_commands_data:
                    for data in korniszon_commands_data:

                        # look for user who made a command in users list, to check if his cooldown has ended for him
                        cooldown = Cooldown.find_user(data['user'])
                        korniszon.rate_korniszon(data, cooldown)
                        cooldown.start() # if cooldown is over and rating a korniszon is attempted, turn on the flag again.


                spam_commands_data = Command.get_commands_by_type(str(spam_command))

                if spam_commands_data:
                    for data in spam_commands_data:
                        spam_korniszon.set_spamming_time(driver, data)


                topniszon_commands_data = Command.get_commands_by_type(str(topniszon_command))

                if topniszon_commands_data:
                    for data in topniszon_commands_data:
                        topniszon.best_korniszon_by_day(data, leaderboard)


                ranking_commands_data = Command.get_commands_by_type(str(ranking_command))

                if ranking_commands_data:
                    data = ranking_commands_data[0]

                    # leaderboard.display_leaderboard(data["input"])
                    t2 = threading.Thread(target=leaderboard.display_leaderboard, args=(data["input"],), daemon=True)
                    t2.start()
                    


                user_stats_data = Command.get_commands_by_type(str(staty_command))

                if user_stats_data:
                    for data in user_stats_data:
                        leaderboard.display_user_stats(data)



                strona_data = Command.get_commands_by_type(str(strona_command))

                if strona_data:
                    response = f"https://www.garneck.pl"
                    wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", response)



                help_commands_data = Command.get_commands_by_type(str(help_command))

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