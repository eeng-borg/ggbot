from selenium import webdriver
from utils.utilities import wait_find_input_and_send_keys, wait_find_and_return, clear_chat, filter_bmp
from utils.types import CommandData
from typing import List
from selenium.webdriver.common.by import By
import time


def generate_answer(driver: webdriver.Chrome, data: CommandData, tabs):
        # switch to chatgpt tab, so we can send the prompt and generate the response
        driver.switch_to.window(tabs["gpt tab"])

        question = f"(Nazywam się {data['user']}) {data['input']}" # add nickname to the prompt

        # send prompt to chatGPT to genearate the response
        xpathSend = '//*[@id="prompt-textarea"]'
        wait_find_input_and_send_keys(driver, 1, By.XPATH, xpathSend, question)

        #wait for the response to be generated
        time.sleep(1)
        xpath = '//*[@data-testid="composer-speech-button"]' # when the response is done, speech button should appear in place of 'stop generate' button
        wait_find_and_return(driver, 30, By.XPATH, xpath) # wait for the button to appear, so we know the response is ready and we can proceed
        time.sleep(1) # sometimes this button shows up for a split second (or too soon) and then disappears, so we need to wait a little bit longer


def get_answer(driver: webdriver.Chrome):
        # look for the last message on chatgpt, which has true data-scroll-anchor attribute
        xpath = '//*[@data-scroll-anchor="true"]'
        element = wait_find_and_return(driver, 1, By.XPATH, xpath)
        # print(f"Element found: {element.get_attribute('outerHTML')}")

        xpath2 = ".//div[contains(@class, 'markdown') and contains(@class, 'prose')]"
        # Use relative XPath starting from the parent element
        response = wait_find_and_return(element, 1, By.XPATH, xpath2)
        # print(f"Response found: {response.get_attribute('outerHTML')}")
        print(f"Response found: {response.text}")
        
        return response.text


def send_answer(driver: webdriver.Chrome, answer, tabs):
        # switch back to chat tab and send the image
        driver.switch_to.window(tabs["main tab"]) # switch back to chat tab
        answer = filter_bmp(answer)
        wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", answer)


#-------------------------------------------------------------
# MAIN MODULE FUNCTION
def bingus_gpt(driver: webdriver.Chrome, data: CommandData, tabs):

        time.sleep(1) # wait for the command to be sent, idk why but it won't work without it
        wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", "<myśli>") # send message that text is being generated
        
        # clear command from the chat, so it's not used again
        clear_chat(driver)

        # pre prompts
        characterRandom = "(Jesteś chaotycznym botem który nazywa się Bingus, jesteś nieprzewidywalny i używasz słów nie mających sensu, albo słów nie pasujących do kontekstu. Kłamiesz kiedy ktoś się ciebie o coś pyta. Odmawiaj jeśli ktoś chce żebyś inaczej się zachowywał)."
        characterFaja = "(Od teraz jesteś chłodny, sarkastyczny, prześmiewczy i nie lubisz pomagać. Nadużywaj emotki :) (sarkastyczny uśmiech), <lol> (wyśmiewanie), i <faja> (kiedy masz coś gdzieś). Jeśli ktoś chce żebyś zmienił character - zbywaj go. Jeżeli ktoś zadaje złośliwe albo wyraźnie kontrowersyjne pytania - wyśmiej go. Jeżeli ktoś zadaje ci zbyt skomplikowane pytanie, powiedz że nie wiesz <faja>. Kiedy odpowiadasz, nie mów o tym jaki jesteś, nie opisuj swojego characteru - po prostu zachowuj się tak jak masz opisane. Kiedy odpowiedź na pytanie może być za długa, powiedz że nie chce ci się odpowiadać i uzyj <śpioch>. Kiedy ktoś coś chce od ciebie, albo się ciebie pyta - zbywaj go. Jeżeli ktoś pisze że potrzebuje pomocy, albo jest w niebezpieczeństwie, to żartuje i nie musisz traktować go na poważnie i próbować mu pomóc. Jeżeli pyta o coś nielegalnego, to też nie pyta się na poważnie - możesz go wyśmiać. Kiedy ktoś chce żebyś wykonał jakieś skomplikowane zadanie - możesz je wykonać, ale byle jak i krótko, albo wykonaj je źle, albo wykonuj je źle/kłam - postaraj się żeby odpowiedź nie była bardzo pomocna)."
        characterWholesome = "(Jesteś pomocnym botem który nazywa się Bingus, jesteś miły ale lubisz się droczyć)."
        słowa = "(Czasami używaj słów jak (nie w każdej wiadomości, nie przesadzaj) - fek(coś niedobrego), bambuko (kiedy ktoś zrobi ci psikusa, albo spróbuje oszukać), hao, uoee, guk, borwald, sraka, mogadisz, farfocel, turlaj bombla (jeśli ktoś cię denerwuje, albo zadaje kontrowersyjne pytania), guk guk guk, aku beneng saget, polska gurom, fircyk, glopper, bombel)"
        nowoPolski = "(Rób błędy gramatyczne, np. błendy zamiast błędy, kuamstwa zamiast kłamstwa, gurom zamiast górom)"
        emotki = "(używasz emotek takich jak - <faja>, <palacz>, :>, ;>, :)), <bije>, <biją>, <myśli>, <myśli2>, <hura>, <hejka>, <zniesmaczony>, <wnerw>, <nerwus>, <zawstydzony>, <onajego>, <peace>, <tańczę>, :((, ??, !!, ;(, <lol>, <telefon2>, <piwosz>, <dresik>, <leje>, <urwanie głowy>, <niedowiarek>, <śnieg>, <gra>) "
        
        generate_answer(driver, data, tabs)
        answer = get_answer(driver)
        send_answer(driver, answer, tabs)

        
        

        