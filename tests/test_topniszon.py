import pytest
from selenium import webdriver
from command_modules.korniszon_module import leaderboard
from command_modules.korniszon_module.korniszon import Korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from command_modules.korniszon_module.topniszon import Topniszon



@pytest.fixture(scope='module')
def mock_topniszon():
    driver = webdriver.Chrome()
    topniszon = Topniszon(driver)
    return topniszon


@pytest.fixture(scope='module')
def mock_leaderboard():
    leaderboard = Leaderboard()
    return leaderboard


def dummy_wait_find_input_and_send_keys(*args):
    pass



@pytest.mark.parametrize("input, result", [
    ("", 'dziś'),
    ("5", "z 5 dnia tego miesiąca"),
    ("gfgg", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."),
    ("14g", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."),
    ("14 5", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."),
    ])

def test_input_to_when(mock_topniszon: Topniszon, input, result):

    when = mock_topniszon._input_to_when(input, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    assert when == result


        
