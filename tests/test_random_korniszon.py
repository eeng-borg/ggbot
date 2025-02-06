import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest.mock import MagicMock, patch
from command_modules.korniszon_module.random_korniszon import SpamKorniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from utils.utilities import async_wait_find_input_send_keys, wait_find_input_and_send_keys

# @pytest.fixture(scope="class")
# def mock_driver():
#     driver = webdriver.Chrome()
#     yield driver


# @pytest.fixture(scope="class")
# def mock_spam_korniszon(mock_driver):

#     leaderbord = Leaderboard()
#     yield SpamKorniszon(mock_driver, leaderbord)

# @pytest.fixture
# def mock_spam_time():
#     yield SpamKorniszon.spam_time


# # @patch('command_modules.korniszon_module.random_korniszon.wait_find_input_and_send_keys')
# def test_set_spamming_time_valid_input(mock_spam_korniszon, mock_driver):

#     command_data = {'input': '45'}
#     mock_spam_korniszon.set_spamming_time(mock_driver, command_data)
    
#     assert SpamKorniszon.spam_time == 45


# # @patch('command_modules.korniszon_module.random_korniszon.wait_find_input_and_send_keys')
# def test_set_spamming_time_invalid_input(mock_spam_korniszon, mock_driver, mock_spam_time):
#     command_data = {'input': 'invalid'}
#     mock_spam_korniszon.set_spamming_time(mock_driver, command_data)
    
#     assert SpamKorniszon.spam_time == mock_spam_time


# # @patch('command_modules.korniszon_module.random_korniszon.wait_find_input_and_send_keys')
# def test_set_spamming_time_below_limit(mock_spam_korniszon, mock_driver, mock_spam_time):
#     command_data = {'input': '0'}
#     mock_spam_korniszon.set_spamming_time(mock_driver, command_data)
    
#     assert SpamKorniszon.spam_time == mock_spam_time
