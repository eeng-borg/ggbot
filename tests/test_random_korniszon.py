from concurrent.futures import thread
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from command_modules.korniszon_module import leaderboard
from command_modules.korniszon_module.random_korniszon import SpamKorniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
import tempfile
import os
import json
import time
import threading
from sql_database import Database


def dummy_wait_find_input_and_send_keys(*arg):
    pass


@pytest.fixture
def mock_driver():
    driver = webdriver.Chrome()
    return driver


@pytest.fixture
def mock_leaderboard():

    database = Database()
    leaderboard = Leaderboard(database=database)
    return leaderboard


@pytest.fixture
def mock_random_korniszon(mock_leaderboard):
    database = Database()
    spamniszon = SpamKorniszon(
        database=database, 
        leaderboard=mock_leaderboard, 
        wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    
    return spamniszon




class TestCreateFileIfNone:

    def test_create_file_if_none_creates_file(self, mock_random_korniszon: SpamKorniszon):

        with tempfile.TemporaryDirectory() as tempdir:
            file_name = os.path.join(tempdir, 'settings.json')
            settings_dict = {}

            mock_random_korniszon._create_file_if_none(file_name, settings_dict)

            assert os.path.exists(file_name)
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert data['spam_time'] == 41



    def test_create_file_if_none_does_not_overwrite_existing_file(self, mock_random_korniszon: SpamKorniszon):

        with tempfile.TemporaryDirectory() as tempdir:
            file_name = os.path.join(tempdir, 'settings.json')
            settings_dict = {'spam_time': 10}

            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(settings_dict, f, indent=4)

            mock_random_korniszon._create_file_if_none(file_name, settings_dict)

            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert data['spam_time'] == 10



class TestGetSpamTime:

    def test_get_spam_time_reads_existing_value(self, mock_random_korniszon: SpamKorniszon):
        with tempfile.TemporaryDirectory() as tempdir:
            file_name = os.path.join(tempdir, 'settings.json')
            settings_dict = {'spam_time': 10}

            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(settings_dict, f, indent=4)

            spam_time = mock_random_korniszon._get_spam_time(file_name, None)
            assert spam_time == 10


    def test_get_spam_time_updates_value(self, mock_random_korniszon: SpamKorniszon):
        with tempfile.TemporaryDirectory() as tempdir:
            file_name = os.path.join(tempdir, 'settings.json')
            settings_dict = {'spam_time': 10}

            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(settings_dict, f, indent=4)

            new_spam_time = 20
            spam_time = mock_random_korniszon._get_spam_time(file_name, new_spam_time)
            assert spam_time == new_spam_time

            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                assert data['spam_time'] == new_spam_time


# check debug console for results
def test_spamming(mock_random_korniszon: SpamKorniszon, mock_leaderboard: Leaderboard):

    mock_leaderboard.leaderboard = [{'input': 'fgfgfgfg'},{'input': 'aav'},{'input': 'ughmm'},]

    # mock_random_korniszon.spam_limit = -100
    mock_random_korniszon.set_spamming_time(input=1)

    time.sleep(2)

    assert mock_random_korniszon.spam_time_left == 2

    mock_random_korniszon.keep_spamming = False




