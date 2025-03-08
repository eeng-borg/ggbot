from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

base_wait_time = 20

##functions
# find element by type and wait until it is clickable
def wait_find_and_click(context, waitTime, by, elementName):
    # for attempt in range(3):  # Retry up to 3 times
    #     try:
            # Wait until the element is clickable
    WebDriverWait(context, waitTime + base_wait_time).until(
        EC.element_to_be_clickable((by, elementName))
    )
    # Locate and click the element
    element = context.find_element(by, elementName)
    element.click()

    
    return element
        


# wait until input bar has loaded, look for it and send text with ENTER
def wait_find_input_and_send_keys(context, waitTime, by, elementName, inputText, send=True):
    # for attempt in range(3):  # Retry up to 3 times
    #     try:
            # Wait for the element to be present
    WebDriverWait(context, waitTime + base_wait_time).until(
        EC.presence_of_element_located((by, elementName))
    )
    # Find and interact with the element
    element = context.find_element(by, elementName)
    element.clear()

    # Copy text to clipboard
    pyperclip.copy(inputText)
    
    # Use keyboard shortcuts to paste
    element.send_keys(Keys.CONTROL, 'v')
    
    # Send Enter if needed
    if send:
        element.send_keys(Keys.ENTER)




# find element by type and return it
def wait_find_and_return(context, waitTime, by, elementName):
    WebDriverWait(context, waitTime + base_wait_time).until(
        EC.presence_of_element_located((by, elementName))
    )
    element = context.find_element(by, elementName)
    return element



def filter_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)



def clear_chat(driver):
    toolbar = wait_find_and_return(driver, 1, By.CLASS_NAME, "toolbar-right") # find chat toolbar
    wait_find_and_click(toolbar, 1, By.CLASS_NAME, "settings-btn") # click on settings button
    wait_find_and_click(driver, 1, By.CLASS_NAME, "clear-all") # click on clear all messages