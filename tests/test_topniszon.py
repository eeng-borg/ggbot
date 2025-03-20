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
def mock_leaderboard(mock_leaderboard_list):
    database = Database()
    leaderboard = Leaderboard(database, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    leaderboard.leaderboard = mock_leaderboard_list
    return leaderboard



@pytest.fixture(scope='module')
def mock_topniszon(mock_leaderboard):
    database = Database()
    driver = webdriver.Chrome()
    topniszon = Topniszon(database=database, leaderboard=mock_leaderboard, driver=driver, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    return topniszon



@pytest.fixture(scope='module')
def mock_leaderboard_list():
    return [
    {
        "id": 1,
        "user": "Zefir",
        "input": "mavlah",
        "score": 742.24,
        "created": "2025-02-24 13:48:00",
        "position": 1
    },
    {
        "id": 267,
        "user": "Marcin",
        "input": "halmav",
        "score": 499.36,
        "created": "2025-02-24 16:13:00",
        "position": 256

    },
    {
        "id": 607,
        "user": "Ing",
        "input": "hu\u0107pa",
        "score": 446.56,
        "created": "2025-02-24 16:18:00",
        "position": 607
    },
    {
        "id": 16,
        "user": "Tadeusz",
        "input": "bilbad",
        "score": 639.84,
        "created": "2025-02-23 18:58:00",
        "position": 16
    },
    {
        "id": 1099,
        "user": "Ing",
        "input": "gromix",
        "score": 398.8,
        "created": "2025-02-23 17:10:00",
        "position": 1099
    },
    {
        "id": 22,
        "user": "Marcin",
        "input": "boralt",
        "score": 620.56,
        "created": "2025-02-19 21:51:00",
        "position": 22
    },
    {
        "id": 95,
        "user": "Zefir",
        "input": "boron",
        "score": 557.56,
        "created": "2025-02-19 12:59:00",
        "position": 95

    }, 
    {
        "position": 11359,
        "user": "Zefir",
        "input": "nieliczony worstniszon",
        "created": "2025-02-19 13:48:00",
        "score": 0.0,
        "position": 11359,
    }
    ]





@pytest.mark.parametrize("input, result", [
    ("", 'dziś'),
    ("5", "z 5 dnia tego miesiaca"),
    ("gfgg", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiaca chciałbyś topniszona, np /topniszon 5."),
    ("14g", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiaca chciałbyś topniszona, np /topniszon 5."),
    ("14 5", "Niepoprawny format <okok>, wprowadź pojedyńcze liczbę z jakiego dnia tego miesiaca chciałbyś topniszona, np /topniszon 5."),
    ])

def test_input_to_when(mock_topniszon: Topniszon, input, result):

    when = mock_topniszon._input_to_when(input)
    assert when == result


@pytest.mark.parametrize("input, result", [
    ('', "Najlepszy dziś <paker>\n1. mavlah - 742.24 (Zefir) o 13:48"),
    ("23", "Najlepszy z 23 dnia tego miesiaca <paker>\n16. bilbad - 639.84 (Tadeusz) o 18:58"),
    ("19", "Najlepszy z 19 dnia tego miesiaca <paker>\n23. boralt - 620.56 (Marcin) o 21:51"),
    ])

def test_best_korniszon_by_day(mock_topniszon: Topniszon, input, result):

    message = mock_topniszon.best_korniszon_by_day(input, best=True, datetime_now=datetime.fromtimestamp(1740401280)) # 24.02.2025 13:48
    assert message == result



@pytest.mark.parametrize("input, result", [
    ('', "Najgorszy dziś <wyśmiewacz>\n267. halmav - 499.36 (Marcin) o 16:13"),
    ("23", "Najgorszy z 23 dnia tego miesiaca <wyśmiewacz>\n333. vargaz - 486.88 (Tadeusz) o 20:56"),
    ("19", "Najgorszy z 19 dnia tego miesiaca <wyśmiewacz>\n95. boron - 557.56 (Zefir) o 12:59"),
    ])

def test_worst_korniszon_by_day(mock_topniszon: Topniszon, input, result):

    message = mock_topniszon.best_korniszon_by_day(input, best=False, datetime_now=datetime.fromtimestamp(1740401280)) # 24.02.2025 13:48
    assert message == result

        
