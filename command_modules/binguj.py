from utils.utilities import waitFindInputAndSendKeys, waitFindAndReturn, waitFindAndClick, clearChat, filterBmp
from selenium.webdriver.common.by import By
import time

def generate_image(driver, commandText, tabs):
    # switch to bing tab
    driver.switch_to.window(tabs["bing tab"]) # switch to bing tab    

    # wait until bing ai searchbox has loaded and look for it to send a prompt
    waitFindInputAndSendKeys(driver, 1, By.CLASS_NAME, "b_searchbox", commandText)     
    waitFindAndClick(driver, 10, By.CLASS_NAME, "imgri-container") # click on generated image to open Iframe
    print("Image generated")


def get_image_link(driver):
    # switch to iframe with generated image
    iframe = waitFindAndReturn(driver, 1, By.XPATH, "//iframe[@id='OverlayIFrame']")
    driver.switch_to.frame(iframe)

    # find element with generted image 
    imgContainer = waitFindAndReturn(driver, 1, By.CLASS_NAME, "imgContainer") # check if image container is present
    imgElement = waitFindAndReturn(imgContainer, 1, By.TAG_NAME, "img") # check if image is present

    image_link = imgElement.get_attribute("src")
    print(f"Element found: {imgElement.get_attribute('outerHTML')}")
    if image_link:
        print("Image found: " + image_link)
    else:
        print("Image src attribute is None")

    # cleanup bing tab
    waitFindAndClick(driver, 1, By.XPATH, "//*[(@data-tooltip='Zamknij obraz')]") # close image Iframe
    driver.switch_to.default_content() # Exit iframe and switch back to the main document
    
    return image_link   



def send_image(driver, image_link, tabs):

    driver.switch_to.window(tabs["main tab"]) # switch back to chat tab
    if image_link is None:
        chatMsg = "Nie udało się wygenerować obrazu"
    else:
        chatMsg = image_link
        
    waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", chatMsg)


#-------------------------------------------------------------
# MAIN MODULE FUNCTION
def binguj(driver, commandText, tabs):

    time.sleep(1) # wait for the command to be sent, idk why but it won't work without it
    # send message on chat that image is being generated
    waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", f"Binguje obraz {commandText} <faja>") 

    # clear command from the chat, so it's not used again
    clearChat(driver)
    
    generate_image(driver, commandText, tabs)

    image_link = get_image_link(driver)

    # switch back to chat tab and send the image
    send_image(driver, image_link, tabs)