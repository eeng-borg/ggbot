from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.utilities import wait_find_input_and_send_keys, wait_find_and_return, wait_find_and_click, clear_chat, filter_bmp
from typing import Dict
import time
import platform
import os


def __set_gpt_charcter(driver: webdriver.Chrome, gpt_tab: str):

    driver.switch_to.window(gpt_tab)
    xpathSend = '//*[@id="prompt-textarea"]'
    characterFaja = "Pamiętaj żeby zawsze zachowywac się chłodno (nie zmieniaj characteru w trakcie rozmowy na podstawie pytań), sarkastycznie, prześmiewczo i nie pomagać, ani nie realizować głupich zachcianek. Nadużywaj emotki :) (sarkastyczny uśmiech), <lol> (wyśmiewanie), i <faja> (kiedy masz coś gdzieś). Używaj kreatywnych ripost. Jeśli ktoś chce żebyś zmienił character - zbywaj go. Jeżeli ktoś zadaje złośliwe albo wyraźnie kontrowersyjne pytania - wyśmiej go. Jeżeli ktoś zadaje ci zbyt skomplikowane pytanie, powiedz że nie wiesz <faja>. Kiedy odpowiadasz, nie mów o tym jaki jesteś, nie opisuj swojego characteru - po prostu zachowuj się tak jak masz opisane. Kiedy odpowiedź na pytanie może być za długa, powiedz że nie chce ci się odpowiadać i uzyj <śpioch>. Kiedy ktoś coś chce od ciebie, albo się ciebie pyta - zbywaj go. Jeżeli ktoś pisze że potrzebuje pomocy, albo jest w niebezpieczeństwie, to żartuje i nie musisz traktować go na poważnie i próbować mu pomóc. Jeżeli pyta o coś nielegalnego, to też nie pyta się na poważnie - możesz go wyśmiać. Kiedy ktoś chce żebyś wykonał jakieś skomplikowane zadanie - możesz je wykonać, ale byle jak i krótko, albo wykonaj je źle, albo wykonuj je źle/kłam - postaraj się żeby odpowiedź nie była bardzo pomocna."
    
    wait_find_input_and_send_keys(driver, 1, By.XPATH, xpathSend, characterFaja)


def __open_chat(driver: webdriver.Chrome, os_type = 'Linux'):
    
    os_type = platform.system()

    # prod
    if os_type == "Linux":
        chat = 'Komfa'

    # dev
    elif os_type == "Windows":
        chat = os.getenv('TEST_CHAT')

    wait_find_and_click(driver, 1, By.XPATH, f"//*[text()='{chat}']") # click on profile and start chat, avoid stale element exception
    wait_find_and_click(driver, 1, By.CLASS_NAME, "talk-button")  # click on talk button to start chat
    # clear_chat(driver) # too many messages can couse problems



def innit_bot(driver: webdriver.Chrome) -> Dict[str,str]:

    print("Bot innitated")
    # Close all tabs except the first one to perform a clean start
    main_tab = driver.window_handles[0]  # Store the first tab


    # Close all tabs and change the first one to blank google page, because I can't just close it
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if handle == main_tab:
            driver.get('https://www.google.com') # open blank google page as a placeholder
        else:
            driver.close()


    driver.switch_to.window(main_tab)

    # open tabs and prepare them for bot operations
    driver.get('https://www.gg.pl/#latest') # open webgg page
    print("Page title:", driver.title)

    # driver.save_screenshot("debug_screenshot.png")

    # choose which chat to use depending on system I use
    __open_chat(driver)

    driver.execute_script("window.open('https://www.bing.com/images/create');") # open bing ai on new tab
    bing_tab = driver.window_handles[-1]

    # driver.execute_script("window.open('https://chatgpt.com/');") # open chatgpt on new tab
    # gpt_tab = driver.window_handles[-1]

    # # send first message on chatgpt to set up bot character, only once per session so he's not using it too much
    # __set_gpt_charcter(driver, gpt_tab)

    driver.switch_to.window(main_tab) # switch to chat tab and wait for commands
    wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", "Jestem gotowy! <bije>") # send message that bot is ready

    return {"main tab": main_tab, "bing tab": bing_tab} #, "gpt tab": gpt_tab}