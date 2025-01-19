from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sys
import random
import os
from selenium.common.exceptions import TimeoutException, WebDriverException
from utils.utilities import waitFindInputAndSendKeys, waitFindAndReturn, waitFindAndClick, clearChat, filterBmp
from innitBot import initBot

from command_modules.binguj import binguj
from command_modules.bingusGpt import bingusGpt
from command_modules.zaczepiacz import zaczepiacz
from command_modules.help import help
from command_modules.korniszon_module.korniszon import korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard

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

# main loop for bot operations
while(True):
    # for testing purposes automatically send command
    # WaitFindInputAndSendKeys(driver, 5, By.ID, "chat-text", "/binguj gf fdfd")
    # time.sleep(1) # wait for the command to be sent

    command_list = []
    #xpaths for commands
    def commandXpath(command_name : str, description: str, text_after_command : bool):
        
        # temp solution
        global command_list
        xpath = ""

        if(text_after_command == True):

            xpath = ( #image generation command
            "//*[@class='ml__item-part-content' " #check if command is in the active chat
            f"and starts-with(normalize-space(text()), '/{command_name} ') " #check if command starts with '/binguj '
            f"and string-length(normalize-space(text())) > string-length('/{command_name} ')]" #check if command is not empty after '/binguj '
            )

        # for commands like 'restart' which don't need additional instructions 
        else:
            xpath = (
            "//*[@class='ml__item-part-content' "
            f"and normalize-space(text())='/{command_name}']"
            )
        
        # make list of all command names and it description to use it in /help
        command_list.append(f"/{command_name} - {description}")

        return xpath
    
    bingujXpath = commandXpath('binguj', "wpisz prompty na obrazek jaki chcesz wygenerować :)", True)
    gptXpath = commandXpath('bingus', "zapytaj się bingusa o cokolwiek, może pomoże ;>", True)
    korniszonXpath = commandXpath('korniszon', "pokaż swojego korniszona, ocenimy uczciwie ;))", True)
    rankingtXpath = commandXpath('ranking', "ranking dwudziestu najpotężniejszych korniszonów w kosmosie!!", False)
    restartXpath = commandXpath('restart', "gdyby się zawiesiło coś, gdzieś", False)
    helpXpath = commandXpath('help', "pokazuje wszystkie komendy, ale skoro już tu jesteś to wiesz co robi :]", False)

    # /bingus
    # find nick of the user who sent the command, if someone wrote few messages in a row, you have to look for his first message to get the element with the nick
    def findGptCommandsAndUserNick():
        messages = driver.find_elements(By.CLASS_NAME, "ml__item--incoming")
        commandFound = False
        gptPrompts = []

        if messages:
            gptPromptText = ""
            for message in reversed(messages):
                gptCommand = message.find_elements(By.XPATH, f".{gptXpath}") # wait until command is found and make list of them

                # check if user has sent a gpt command and turn on a switch, so we can look for a nick of the user
                if gptCommand:
                    print(f"Wiadomość: {gptCommand[0].text}")
                    gptPromptText = gptCommand[0].text.replace("/bingus ", "") # remove /binguj from the command, so we can use it as a prompt
                    commandFound = True

                # look for nick only if user sent a command
                if commandFound:
                    nick = message.find_elements(By.CLASS_NAME, "ml__item-username")
                    print(f"Nick found: {len(nick)}")

                    if nick:
                        print(f"Nick: {nick[0].text}")
                        gptPromptText = f"(Nazywam się {nick[0].text})  {gptPromptText}" # add nick to the prompt, so bot knows who is asking
                        print (f"Pełna wiadomość: {nick[0].text} napisał, {gptPromptText}")
                        gptPrompts.append(gptPromptText) # add prompt to the list of prompts to
                        commandFound = False # turn off the switch if nick is found, so we don't look it while waiting for another command
        
        # we are filtering out unsupported characters from the prompt list, so there's no error while sending it with selenium
        return [filterBmp(prompt) for prompt in gptPrompts]

    # /binguj
    bingujCommands = driver.find_elements(By.XPATH, bingujXpath) # wait until command is found and make list of them
    bingPrompts = [command.text.replace("/binguj ", "") for command in bingujCommands] if bingujCommands else [] # process commands from the list into a list of strings, which can be used as prompts
    bingPrompts = [filterBmp(text) for text in bingPrompts]

    # /korniszon
    korniszonCommand = driver.find_elements(By.XPATH, korniszonXpath)
    korniszon_text = [command.text.replace("/korniszon ", "") for command in korniszonCommand] if korniszonCommand else [] # process commands from the list into a list of strings, which can be used as prompts
    korniszon_text = [filterBmp(text) for text in korniszon_text]

    # /ranking
    rankingCommand = driver.find_elements(By.XPATH, rankingtXpath)

    # /restart
    restartCommand = driver.find_elements(By.XPATH, restartXpath)

    # /help
    helpCommand = driver.find_elements(By.XPATH, helpXpath)

    # -zaczepka
    # im looking for the messages without 'continue' class, because those are the only messages with user nickname in it,
    # so I know who wrote it and I can use it to poke someone by username.
    # firstMessages = driver.find_elements(By.XPATH, "//*[@class='ml__item ml__item--incoming']") # incoming are messages from other users than me
    
    # if there's a message I looked for, we can roll the dice if we want to start conversation with someone
    # if there are more than one messages, I'll take only the last one - for similicity sake
    # makeZaczepka = False
    # if firstMessages:
    #     username = firstMessages[-1].find_elements(By.CLASS_NAME, "ml__item-username") # looking for username in the last element from the list
    #     message = firstMessages[-1].find_elements(By.CLASS_NAME, "ml__item-part-content") # looking for message in the last element from the list
    #     zaczepkaPrompt = (f"(Nazywam się {username[0].text}) {message[0].text}") # combining message and username to make a prompt for the bot
    #     # print(f"Zaczepka: {zaczepkaPrompt}")

    #     rolledNumber = random.randint(1, 10000) #once for x minutes on average 10k = 5min
    #     # print(f"Rolled number: {rolledNumber}")
    #     chance = 1
    #     if rolledNumber <= chance:
    #         makeZaczepka = True

    # try to catch exceptions if command is found
    try:
        # check if binguj command is found and execute it
        if bingujCommands:
            for prompt in bingPrompts:
                binguj(driver, prompt)  # Call Binguj function with the command as an argument
        
        # check if chatgpt command is found and execute it
        elif findGptCommandsAndUserNick():
            for prompt in findGptCommandsAndUserNick():
                bingusGpt(driver, prompt)
        
        elif korniszonCommand:
            korniszon(driver, korniszon_text[0])

        elif rankingCommand:
            clearChat(driver)
            leaderboard = Leaderboard()
            leaderboard.load_leaderboard()
            leaderboard.display_leaderboard(driver)
            
        
        # elif makeZaczepka:
        #     zaczepiacz(driver, zaczepkaPrompt)

        #restart a bot
        elif restartCommand:
            clearChat(driver)
            waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", "Restartuje się <palacz>")
            initBot(driver)            

        elif helpCommand:
            help(driver, command_list)
            clearChat(driver) # list of commands can trigger some commands



    except TimeoutException:
        print("Timeout occurred while executing function")
        driver.switch_to.window(driver.window_handles[0])
        safe_text = prompt if isinstance(prompt, str) else str(bingPrompts)
        waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", f"Nie udało się wybingować {safe_text} ;(")
        continue

    # except WebDriverException as e:
    #     if "ChromeDriver only supports characters in the BMP" in str(e):
    #         print(f"Unsupported characters detected in: {prompt}")
    #         WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", f"Niedozwolone znaki <zniesmaczony>")
    #         clearChat(driver)
    #     else:
    #         print(f"WebDriverException: {e}")
    #     driver.switch_to.window(driver.window_handles[0])
    #     continue

    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}, {e}")
        driver.switch_to.window(driver.window_handles[0])
        continue

    # input("Press Enter to exit...")
