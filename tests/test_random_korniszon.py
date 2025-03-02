import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest.mock import MagicMock, patch
from command_modules.korniszon_module import leaderboard
from command_modules.korniszon_module.random_korniszon import SpamKorniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
import tempfile
import os
import json

# @pytest.fixture
# def mock_random_korniszon():
#     driver = webdriver.Chrome()
#     leaderboard = Leaderboard(driver)
#     spamniszon = SpamKorniszon(driver, leaderboard)


@pytest.fixture
def mock_random_korniszon():
    driver = webdriver.Chrome()
    leaderboard = Leaderboard(driver)
    spamniszon = SpamKorniszon(driver, leaderboard)
    return spamniszon



def test_create_file_if_none_creates_file(mock_random_korniszon: SpamKorniszon):

    with tempfile.TemporaryDirectory() as tempdir:
        file_name = os.path.join(tempdir, 'settings.json')
        settings_dict = {}

        mock_random_korniszon._create_file_if_none(file_name, settings_dict)

        assert os.path.exists(file_name)
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data['spam_time'] == 41



def test_create_file_if_none_does_not_overwrite_existing_file(mock_random_korniszon: SpamKorniszon):

    with tempfile.TemporaryDirectory() as tempdir:
        file_name = os.path.join(tempdir, 'settings.json')
        settings_dict = {'spam_time': 10}

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(settings_dict, f, indent=4)

        mock_random_korniszon._create_file_if_none(file_name, settings_dict)

        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data['spam_time'] == 10


def test_get_spam_time_reads_existing_value(mock_random_korniszon: SpamKorniszon):
    with tempfile.TemporaryDirectory() as tempdir:
        file_name = os.path.join(tempdir, 'settings.json')
        settings_dict = {'spam_time': 10}

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(settings_dict, f, indent=4)

        spam_time = mock_random_korniszon._get_spam_time(file_name, None)
        assert spam_time == 10


def test_get_spam_time_updates_value(mock_random_korniszon: SpamKorniszon):
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


