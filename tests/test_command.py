import pytest
from unittest.mock import patch
from unittest.mock import Mock
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium import webdriver
from command_modules.command import Command
from pathlib import Path


class TestGetCommandByType:

    @pytest.fixture(scope="class")
    def setup_class(self):

        driver = webdriver.Chrome()
        command = Command(driver, "test_command", "This is a test command")
        Command.received_commands = [
            {"command": "test_command", "user": "user1", "input": "input1", "time": {}},
            {"command": "another_command", "user": "user2", "input": "input2", "time": {}},
            {"command": "test_command", "user": "user3", "input": "input3", "time": {}}
        ]
        yield command
        driver.quit()
        

    def test_get_commands_by_type_found(self, setup_class):

        command = setup_class
        result = Command.get_commands_by_type("test_command")
        assert len(result) == 2
        assert result[0]["user"] == "user1"
        assert result[1]["user"] == "user3"


    def test_get_commands_by_type_not_found(self, setup_class):

        command = setup_class
        result = Command.get_commands_by_type("non_existent_command")
        assert len(result) == 0



class TestGetCommandData:

    @pytest.fixture(scope="class")
    def get_elements(self, ):

        driver = webdriver.Chrome()

        Command(driver, "korniszon", "This is a test command")
        Command(driver, "help", "dfdfffdf")

        driver.get("file:///C:/Users/gordi/OneDrive/Dokumenty/Python_projects/ggbot/tests/incoming_messages_html/messages.html")
        incoming_messages = driver.find_elements(By.CLASS_NAME, "ml__item--incoming")
        Command.get_commands_data(incoming_messages)

        yield incoming_messages
        driver.quit()


    def test_counting_all(self, get_elements):
        assert len(get_elements) == 6


    def test_counting_commands(self):

        assert len(Command.received_commands) == 5

    # shared params for multiple tests
    @pytest.fixture(params=[
        (0, "Janusz", "julanga", "korniszon"),
        (1, "Mirok", "trmawaj", "korniszon"),
        (2, "Mirok", "uakam.", "korniszon"),
        (3, "ula", "tram.", "korniszon"),
        (4, "ula", "", "help")
    ])
    def command_data(self, request):
        return request.param
    

    def test_user(self, command_data):

        id, user, _, _ = command_data
        assert Command.received_commands[id]['user'] == user


    def test_input(self, command_data):

        id, _, input, _ = command_data
        assert Command.received_commands[id]['input'] == input


    def test_command(self, command_data):
        
        id, _, _, command = command_data
        assert Command.received_commands[id]['command'] == command

