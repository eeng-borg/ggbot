
from utils.utilities import waitFindInputAndSendKeys
from selenium.webdriver.common.by import By

def help(driver, command_list):

    for command_item in command_list:
        waitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", command_item)
