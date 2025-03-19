import pytest
from selenium import webdriver
from command_modules.korniszon_module import leaderboard
from command_modules.korniszon_module.random_korniszon import SpamKorniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from command_modules.korniszon_module.spamnij import Spamnij
from sql_database import Database


def dummy_wait_find_input_and_send_keys(*arg):
    pass

@pytest.fixture
def mock_spamnij():
    
    database = Database()
    return Spamnij(database, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)


@pytest.mark.parametrize("input, exception, exception_msg, quantity, lenght, emota", [
    ("5 3", None, "", 5, 3, False),
    ("2 4 emota", None, "", 2, 4, True),
    ("emota 5 3", None, "", 5, 3, True),
    ("2h 4", True, "Pierwsze dwa inputy muszą być liczbowe :).", 1, 1, False),
    ("2h 4 7", True, "Dej dwa inputy z liczbami kierowniku <prosi>.", 1, 1, False),
    ("2-4", True, "Dej dwa inputy z liczbami kierowniku <prosi>.", 1, 1, False),
    ("2.5 4.1", True, "Pierwsze dwa inputy muszą być liczbowe :).", 1, 1, False),
])
def test_translate_input(mock_spamnij, input, exception, exception_msg, quantity, lenght, emota):

    result = mock_spamnij._translate_input(input)
    assert result is exception
    assert mock_spamnij.exception_response == exception_msg
    assert mock_spamnij.quantity == quantity
    assert mock_spamnij.lenght == lenght
    assert mock_spamnij.emota is emota

