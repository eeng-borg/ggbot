import pytest
from selenium import webdriver
from utils.types import CommandData
from command_modules.korniszon_module.korniszon import Korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from users import Cooldown
from sql_database import Database


@pytest.fixture(scope = 'class')
def mock_driver():

    driver = webdriver.Chrome()
    return driver

def dummy_wait_find_input_and_send_keys(*args, **kwargs):
    return

@pytest.fixture
def mock_leaderboard(mock_driver):
    database = Database()
    leaderboard = Leaderboard(database, mock_driver, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    return leaderboard



@pytest.fixture
def mock_korniszon(mock_driver, mock_leaderboard):
    database = Database()
    korniszon = Korniszon(database, mock_driver, mock_leaderboard)

    return korniszon



class TestAdding:

    
    @pytest.fixture(scope='class')
    def mock_command_data(self):

        data = CommandData(user='Janusz', input='bualoa', command='korniszon', time={'day':1,'month':2,'year':2000,'hour':1,'minute':2})
        return data
    
    
    def dummy_send_results(*args, **kwargs):
        # Return a controlled value instead of triggering a timeout.
        return []  # or a list of dummy elements if needed

    

    def test_adding_new(self, mock_korniszon: Korniszon, mock_command_data, mock_leaderboard: Leaderboard):

        cooldown = Cooldown.find_user(mock_command_data['user'])
        mock_korniszon.rate_korniszon(mock_command_data, cooldown, self.dummy_send_results)

        assert len(mock_leaderboard.leaderboard) == 1



    def test_adding_new2(self, mock_korniszon: Korniszon, mock_command_data, mock_leaderboard: Leaderboard):

        cooldown = Cooldown.find_user(mock_command_data['user'])
        mock_korniszon.rate_korniszon(mock_command_data, cooldown, self.dummy_send_results)

        assert len(mock_leaderboard.leaderboard) == 1




@pytest.mark.parametrize("input, result", [
    ("", {"from_index": 0, "to_index": 10}),
    ("gfgfgfgf", {"from_index": 0, "to_index": 10}),
    ("gfgfgfgf2", {"from_index": 0, "to_index": 2}),
    ("gfgfgfgf 2", {"from_index": 0, "to_index": 2}),
    ("5ffgfgg15", {"from_index": 0, "to_index": 515}),
    ("12", {"from_index": 0, "to_index": 12}),
    ("600 620", {"from_index": 600, "to_index": 620}),
    ("12 20", {"from_index": 12, "to_index": 20}),
    ("60 60", {"from_index": 60, "to_index": 60}),
    ("100 110", {"from_index": 100, "to_index": 110}),
    ])    

def test_get_range_from_input(input, result):

    _result = Leaderboard._get_range_from_input(input)
    assert _result == result



@pytest.fixture
def mock_leaderboard_list():
    return [
            {
        "id": 1,
        "user": "Zefir",
        "input": "mavlah",
        "score": 742.24,
        "created": "2025-02-24 13:48:00"
    },
    {
        "id": 2,
        "user": "Marcin",
        "input": "gurbak",
        "score": 724.48,
        "created": "2025-02-05 12:10:00"
    },
    {
        "id": 3,
        "user": "Zefir",
        "input": "d\u0142ugas",
        "score": 706.96,
        "created": "2025-02-04 23:08:00"
    },
    {
        "id": 4,
        "user": "Tadeusz",
        "input": "vigvan",
        "score": 706.96,
        "created": "2025-02-06 18:12:00"
    },
    {
        "id": 5,
        "user": "Marcin",
        "input": "waturn",
        "score": 698.32,
        "created": "2025-02-03 14:16:00"
    },
    {
        "id": 6,
        "user": "Marcin",
        "input": "falter",
        "score": 696.8,
        "created": "2025-01-31 00:12:00"
    },
    {
        "id": 7,
        "user": "Marcin",
        "input": "mator",
        "score": 694.68,
        "created": "2025-02-05 11:38:00"
    },
    {
        "id": 8,
        "user": "Tadeusz",
        "input": "halvor",
        "score": 677.6,
        "created": "2025-01-25 21:26:00"
    },
    {
        "id": 9,
        "user": "Zefir",
        "input": "gulgot",
        "score": 676.16,
        "created": "2025-02-17 21:42:00"
    },
    {
        "id": 10,
        "user": "Ing",
        "input": "jalong",
        "score": 675.44,
        "created": "2025-02-04 00:49:00"
    },
    {
        "id": 11,
        "user": "Ing",
        "input": "hagen",
        "score": 670.88,
        "created": "2025-01-19 14:27:00"
    },
    {
        "id": 12,
        "user": "Marcin",
        "input": "brudas",
        "score": 660.72,
        "created": "2025-02-02 17:32:00"
    },
    {
        "id": 13,
        "user": "Marcin",
        "input": "laptul",
        "score": 649.76,
        "created": "2025-01-29 16:01:00"
    },
    {
        "id": 14,
        "user": "Marcin",
        "input": "widwan",
        "score": 647.76,
        "created": "2025-02-04 23:39:00"
    },
    {
        "id": 15,
        "user": "Marcin",
        "input": "kurzegatg",
        "score": 644.88,
        "created": "2025-02-04 13:27:00"
    },
    {
        "id": 16,
        "user": "Tadeusz",
        "input": "bilbad",
        "score": 639.84,
        "created": "2025-02-23 18:58:00"
    },
    {
        "id": 17,
        "user": "Garett",
        "input": "ingus",
        "score": 638.4,
        "created": "2025-01-27 22:46:00"
    },
    {
        "id": 18,
        "user": "Tadeusz",
        "input": "garga",
        "score": 630.32,
        "created": "2025-01-19 22:35:00"
    },
    {
        "id": 19,
        "user": "Tadeusz",
        "input": "marton",
        "score": 629.84,
        "created": "2025-02-26 14:39:56"
    },
    {
        "id": 20,
        "user": "Marcin",
        "input": "halkord",
        "score": 626.2,
        "created": "2025-02-06 13:46:00"
    },
    {
        "id": 21,
        "user": "Marcin",
        "input": "mechazord",
        "score": 625.12,
        "created": "2025-02-04 23:21:00"
    },
    {
        "id": 22,
        "user": "Marcin",
        "input": "kwakut",
        "score": 621.12,
        "created": "2025-02-02 19:07:00"
    },
    {
        "id": 23,
        "user": "Marcin",
        "input": "boralt",
        "score": 620.56,
        "created": "2025-02-19 21:51:00"
    },
    {
        "id": 24,
        "user": "Marcin",
        "input": "uwkar",
        "score": 617.84,
        "created": "2025-02-01 18:45:00"
    },
    {
        "id": 25,
        "user": "Marcin",
        "input": "garnel",
        "score": 615.04,
        "created": "2025-01-28 00:04:00"
    },
    {
        "id": 26,
        "user": "Tadeusz",
        "input": "guffer",
        "score": 613.12,
        "created": "2025-02-21 17:55:00"
    },
    {
        "id": 27,
        "user": "Tadeusz",
        "input": "warkon",
        "score": 612.48,
        "created": "2025-02-21 18:35:00"
    },
    {
        "id": 28,
        "user": "Marcin",
        "input": "wilkus",
        "score": 611.28,
        "created": "2025-01-31 00:10:00"
    },
    {
        "id": 29,
        "user": "Marcin",
        "input": "burkar",
        "score": 607.76,
        "created": "2025-02-01 18:46:00"
    },
    {
        "id": 30,
        "user": "Tadeusz",
        "input": "smorat",
        "score": 601.36,
        "created": "2025-02-26 12:50:11"
    },
    {
        "id": 31,
        "user": "Tadeusz",
        "input": "bartok",
        "score": 599.84,
        "created": "2025-01-25 21:26:00"
    },
    {
        "id": 32,
        "user": "Marcin",
        "input": "ingpal",
        "score": 599.68,
        "created": "2025-01-27 19:51:00"
    },
    {
        "id": 33,
        "user": "Marcin",
        "input": "karafka",
        "score": 599.12,
        "created": "2025-01-19 15:06:00"
    },
    {
        "id": 34,
        "user": "Tadeusz",
        "input": "matusz",
        "score": 596.72,
        "created": "2025-01-25 21:13:00"
    },
    {
        "id": 35,
        "user": "Zefir",
        "input": "webber",
        "score": 594.16,
        "created": "2025-02-17 23:20:00"
    },
    {
        "id": 36,
        "user": "Marcin",
        "input": "setkve",
        "score": 589.92,
        "created": "2025-02-01 18:41:00"
    },
    {
        "id": 37,
        "user": "Ing",
        "input": "hutnik",
        "score": 589.44,
        "created": "2025-02-15 18:10:00"
    },
    {
        "id": 38,
        "user": "Marcin",
        "input": "kwikon",
        "score": 589.04,
        "created": "2025-01-27 23:50:00"
    },
    {
        "id": 39,
        "user": "Marcin",
        "input": "xurwa",
        "score": 585.6,
        "created": "2025-01-29 18:54:00"
    },
    {
        "id": 40,
        "user": "Marcin",
        "input": "lubart",
        "score": 584.8,
        "created": "2025-02-04 19:04:00"
    },
    {
        "id": 41,
        "user": "Ing",
        "input": "golgos",
        "score": 583.68,
        "created": "2025-02-21 18:48:00"
    },
    {
        "id": 42,
        "user": "Marcin",
        "input": "rikers",
        "score": 583.2,
        "created": "2025-02-28 15:35:30"
    },
    {
        "id": 43,
        "user": "Marcin",
        "input": "istrak",
        "score": 583.12,
        "created": "2025-02-07 12:26:00"
    },
    {
        "id": 44,
        "user": "Marcin",
        "input": "gliger",
        "score": 582.96,
        "created": "2025-02-02 11:27:00"
    },
    {
        "id": 45,
        "user": "Zefir",
        "input": "gulgak",
        "score": 582.4,
        "created": "2025-02-18 14:51:00"
    },


]



@pytest.mark.parametrize("from_index, to_index, to_index_fixed", [
    (0, 10, 10),
    (0, 40, 30),
    (10, 45, 40),
    ])

def test_check_if_range_is_too_big(mock_leaderboard: Leaderboard, from_index, to_index, to_index_fixed):

    result = mock_leaderboard._check_if_range_is_too_big(from_index, to_index)
    assert result == to_index_fixed




def test_display_leaderboard_default_range(mock_leaderboard: Leaderboard, mock_leaderboard_list):
    mock_leaderboard.leaderboard = mock_leaderboard_list
    
    result = mock_leaderboard.display_leaderboard('')
    # Split the result string into lines and remove any empty lines
    result_lines = [line for line in result.split('\n') if line]
    
    assert len(result_lines) == 10
    
    assert result_lines[0] == '1. mavlah - 742.24 (Zefir)'
    assert result_lines[4] == '5. waturn - 698.32 (Marcin)'
    assert result_lines[9] == '10. jalong - 675.44 (Ing)'



def test_display_leaderboard_custom_range(mock_leaderboard: Leaderboard, mock_leaderboard_list):
    
    mock_leaderboard.leaderboard = mock_leaderboard_list


    result = mock_leaderboard.display_leaderboard("10 40")
    result_lines = [line for line in result.split('\n') if line]
    assert len(result_lines) == 31
    
    
    assert result_lines[3] == '13. laptul - 649.76 (Marcin)'
    assert result_lines[16] == '26. guffer - 613.12 (Tadeusz)'
    assert result_lines[21] == '31. bartok - 599.84 (Tadeusz)'




# def test_display_leaderboard_spamming(mock_leaderboard: Leaderboard, mock_leaderboard_list):
    
#     mock_leaderboard.leaderboard = mock_leaderboard_list


#     result = mock_leaderboard.display_leaderboard("10 40", wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
#     result2 = mock_leaderboard.display_leaderboard("10 20", wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    
#     assert len(result2) == 0
#     assert len(result) == 30

    



