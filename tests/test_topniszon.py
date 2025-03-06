import datetime
import pytest
from selenium import webdriver
from command_modules.korniszon_module import leaderboard
from command_modules.korniszon_module.korniszon import Korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from command_modules.korniszon_module.topniszon import Topniszon
from datetime import datetime
from sql_database import Database



def dummy_wait_find_input_and_send_keys(*args):
    pass



@pytest.fixture(scope='module')
def mock_topniszon():
    driver = webdriver.Chrome()
    topniszon = Topniszon(driver, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    return topniszon



@pytest.fixture(scope='module')
def mock_leaderboard_list():
    return [
    {
        "user": "Zefir",
        "input": "mavlah",
        "time": "24.02.2025 13:48",
        "score": 742.24,
        "position": 1,
        "timestamp": 1740401280
    },
    {
        "user": "Marcin",
        "input": "halmav",
        "time": "24.02.2025 16:13",
        "score": 499.36,
        "position": 256,
        "timestamp": 1740409980
    },
    {
        "user": "Ing",
        "input": "hu\u0107pa",
        "time": "24.02.2025 16:18",
        "score": 446.56,
        "position": 576,
        "timestamp": 1740410280
    },
    {
        "user": "Tadeusz",
        "input": "bilbad",
        "time": "23.02.2025 18:58",
        "score": 639.84,
        "position": 16,
        "timestamp": 1740333480
    },
    {
        "user": "Ing",
        "input": "gromix",
        "time": "23.02.2025 17:10",
        "score": 398.8,
        "position": 1036,
        "timestamp": 1740327000
    },
    {
        "user": "Marcin",
        "input": "boralt",
        "time": "19.02.2025 21:51",
        "score": 620.56,
        "position": 22,
        "timestamp": 1739998260
    },
    {
        "user": "Zefir",
        "input": "boron",
        "time": "19.02.2025 12:59",
        "score": 557.56,
        "position": 90,
        "timestamp": 1739966340
    },    
    {
        "user": "Zefir",
        "input": "nieliczony worstniszon",
        "time": "19.02.2025 13:48",
        "score": 0.0,
        "position": 11359,
        "timestamp": 1739969280
    },]



@pytest.fixture(scope='module')
def mock_leaderboard(mock_leaderboard_list):
    database = Database()
    leaderboard = Leaderboard(database, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    leaderboard.leaderboard = mock_leaderboard_list
    return leaderboard




@pytest.mark.parametrize("input, result", [
    ("", 'dziś'),
    ("5", "z 5 dnia tego miesiąca"),
    ("gfgg", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."),
    ("14g", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."),
    ("14 5", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiąca chciałbyś topniszona, np /topniszon 5."),
    ])

def test_input_to_when(mock_topniszon: Topniszon, input, result):

    when = mock_topniszon._input_to_when(input)
    assert when == result


@pytest.mark.parametrize("input, result", [
    ('', "Najlepszy dziś <paker>\n1. mavlah - 742.24 (Zefir) o 13:48"),
    ("23", "Najlepszy z 23 dnia tego miesiąca <paker>\n16. bilbad - 639.84 (Tadeusz) o 18:58"),
    ("19", "Najlepszy z 19 dnia tego miesiąca <paker>\n22. boralt - 620.56 (Marcin) o 21:51"),
    ])

def test_best_korniszon_by_day(mock_topniszon: Topniszon, input, result, mock_leaderboard: Leaderboard):

    message = mock_topniszon.best_korniszon_by_day(input, mock_leaderboard, datetime_now=datetime.fromtimestamp(1740401280)) # 24.02.2025 13:48
    assert message == result



@pytest.mark.parametrize("input, result", [
    ('', "Najgorszy dziś <wyśmiewacz>\n576. hu\u0107pa - 446.56 (Ing) o 16:18"),
    ("23", "Najgorszy z 23 dnia tego miesiąca <wyśmiewacz>\n1036. gromix - 398.8 (Ing) o 17:10"),
    ("19", "Najgorszy z 19 dnia tego miesiąca <wyśmiewacz>\n90. boron - 557.56 (Zefir) o 12:59"),
    ])

def test_worst_korniszon_by_day(mock_topniszon: Topniszon, input, result, mock_leaderboard: Leaderboard):

    message = mock_topniszon.best_korniszon_by_day(input, mock_leaderboard, best=False, datetime_now=datetime.fromtimestamp(1740401280)) # 24.02.2025 13:48
    assert message == result

        
