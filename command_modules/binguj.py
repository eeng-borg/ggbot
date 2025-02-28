from selenium import webdriver
from utils.utilities import wait_find_input_and_send_keys, wait_find_and_return, wait_find_and_click, clear_chat, filter_bmp
from selenium.webdriver.common.by import By
import time
from typing import Dict


def generate_image(driver: webdriver.Chrome, commandText: str, tabs: Dict[str,str]):
    # switch to bing tab
    driver.switch_to.window(tabs["bing tab"]) # switch to bing tab    

    # wait until bing ai searchbox has loaded and look for it to send a prompt
    wait_find_input_and_send_keys(driver, 1, By.CLASS_NAME, "b_searchbox", commandText)
    wait_find_and_click(driver, 10, By.CLASS_NAME, "imgri-container") # click on generated image to open Iframe
    print("Image generated")


def get_image_link(driver: webdriver.Chrome) -> str|None:

    # switch to iframe with generated image
    iframe = wait_find_and_return(driver, 1, By.XPATH, "//iframe[@id='OverlayIFrame']")
    driver.switch_to.frame(iframe)

    # find element with generted image
    imgContainer = wait_find_and_return(driver, 1, By.CLASS_NAME, "imgContainer") # check if image container is present
    imgElement = wait_find_and_return(imgContainer, 1, By.TAG_NAME, "img") # check if image is present

    image_link = imgElement.get_attribute("src")
    print(f"Element found: {imgElement.get_attribute('outerHTML')}")
    if image_link:
        print("Image found: " + image_link)
    else:
        print("Image src attribute is None")

    # cleanup bing tab
    print("Zamykam obraz") 
    # class="close nofocus"
    wait_find_and_click(driver, 1, By.XPATH, "//*[(@class='close nofocus')]") # close image Iframe
    driver.switch_to.default_content() # Exit iframe and switch back to the main document
    
    print("Obraz zamknięty, zwracam link")
    return image_link



def send_image(driver: webdriver.Chrome, image_link: str|None, tabs: Dict[str,str]):

    driver.switch_to.window(tabs["main tab"]) # switch back to chat tab
    if image_link is None:
        chatMsg = "Nie udało się wygenerować obrazu"
    else:
        chatMsg = image_link
    
    print("Wysyłam obraz na czat")
    wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", chatMsg)


#-------------------------------------------------------------
# MAIN MODULE FUNCTION
def binguj(driver: webdriver.Chrome, commandText: str, tabs: Dict[str,str]):

    time.sleep(1) # wait for the command to be sent, idk why but it won't work without it
    # send message on chat that image is being generated
    wait_find_input_and_send_keys(driver, 1, By.ID, "chat-text", f"Binguje obraz {commandText} <faja>") 

    # clear command from the chat, so it's not used again
    
    generate_image(driver, commandText, tabs)

    image_link = get_image_link(driver)

    # switch back to chat tab and send the image
    send_image(driver, image_link, tabs)