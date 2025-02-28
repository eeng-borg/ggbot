import pytest
from selenium import webdriver
from utils.types import CommandData
from command_modules.korniszon_module.korniszon import Korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from users import Cooldown

# class TestGetUserStats:

#     @pytest.mark.parametrize(["user", "result"], [
#         ("", 0),
#         ("Aku", 4),
#         ("Garond", 3),
#         ("Bombel", 0)
#         ])
#     def test_score_sum(self, user, result):
#         assert leaderboard.leaderboard__get_user_korniszons(user, 1) == result

    # @pytest.mark.parametrize("text", ["oooo", "oaauuiióeęą", "aie ou y"])
    # def test_100_percent(self, text):
    #     assert score_vowels_percent(SharedData.base_score, text) == 0

#     # @pytest.mark.parametrize("text", ["oooo", "oaauuiióeęą", "aie ou y"])
#     # def test_100_percent(self, text):
#     #     assert score_vowels_percent(SharedData.base_score, text) == 0



@pytest.fixture(scope = 'class')
def mock_driver():

    driver = webdriver.Chrome()
    return driver



@pytest.fixture
def mock_leaderboard(mock_driver):

    leaderboard = Leaderboard(mock_driver)
    return leaderboard



@pytest.fixture
def mock_korniszon(mock_driver, mock_leaderboard):

    korniszon = Korniszon(mock_driver, mock_leaderboard)

    return korniszon




def dummy_wait_find_input_and_send_keys(*args, **kwargs):
    return



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
    ("600 620", {"from_index": 599, "to_index": 620}),
    ("12 20", {"from_index": 11, "to_index": 20}),
    ("60 60", {"from_index": 59, "to_index": 60}),
    ("100 110", {"from_index": 99, "to_index": 110}),
    ])    

def test_get_range_from_input(input, result):

    _result = Leaderboard._get_range_from_input(input)
    assert _result == result



@pytest.fixture
def mock_leaderboard_list():
    return [
    {
        "user": "Marcin",
        "input": "gurbak",
        "time": {
            "hour": 12,
            "minute": 10,
            "day": 5,
            "month": 2,
            "year": 2025
        },
        "score": 724.48,
        "position": 1
    },
    {
        "user": "Zefir",
        "input": "d\u0142ugas",
        "time": {
            "hour": 23,
            "minute": 8,
            "day": 4,
            "month": 2,
            "year": 2025
        },
        "score": 706.96,
        "position": 2
    },
    {
        "user": "Tadeusz",
        "input": "vigvan",
        "time": {
            "hour": 18,
            "minute": 12,
            "day": 6,
            "month": 2,
            "year": 2025
        },
        "score": 706.96,
        "position": 3
    },
    {
        "user": "Marcin",
        "input": "waturn",
        "time": {
            "hour": 14,
            "minute": 16,
            "day": 3,
            "month": 2,
            "year": 2025
        },
        "score": 698.32,
        "position": 4
    },
    {
        "user": "Marcin",
        "input": "falter",
        "time": {
            "hour": 0,
            "minute": 12,
            "day": 31,
            "month": 1,
            "year": 2025
        },
        "score": 696.8,
        "position": 5
    },
    {
        "user": "Marcin",
        "input": "mator",
        "time": {
            "hour": 11,
            "minute": 38,
            "day": 5,
            "month": 2,
            "year": 2025
        },
        "score": 694.68,
        "position": 6
    },
    {
        "user": "Tadeusz",
        "input": "halvor",
        "time": {
            "hour": 21,
            "minute": 26,
            "day": 25,
            "month": 1,
            "year": 2025
        },
        "score": 677.6,
        "position": 7
    },
    {
        "user": "Zefir",
        "input": "gulgot",
        "time": {
            "hour": 21,
            "minute": 42,
            "day": 17,
            "month": 2,
            "year": 2025
        },
        "score": 676.16,
        "position": 8
    },
    {
        "user": "Ing",
        "input": "jalong",
        "time": {
            "hour": 0,
            "minute": 49,
            "day": 4,
            "month": 2,
            "year": 2025
        },
        "score": 675.44,
        "position": 9
    },
    {
        "user": "Ing",
        "input": "hagen",
        "time": {
            "hour": 14,
            "minute": 27,
            "day": 19,
            "month": 1,
            "year": 2025
        },
        "score": 670.88,
        "position": 10
    },
    {
        "user": "Marcin",
        "input": "brudas",
        "time": {
            "hour": 17,
            "minute": 32,
            "day": 2,
            "month": 2,
            "year": 2025
        },
        "score": 660.72,
        "position": 11
    },
    {
        "user": "Marcin",
        "input": "laptul",
        "time": {
            "hour": 16,
            "minute": 1,
            "day": 29,
            "month": 1,
            "year": 2025
        },
        "score": 649.76,
        "position": 12
    },
    {
        "user": "Marcin",
        "input": "widwan",
        "time": {
            "hour": 23,
            "minute": 39,
            "day": 4,
            "month": 2,
            "year": 2025
        },
        "score": 647.76,
        "position": 13
    },
    {
        "user": "Marcin",
        "input": "kurzegatg",
        "time": {
            "hour": 13,
            "minute": 27,
            "day": 4,
            "month": 2,
            "year": 2025
        },
        "score": 644.88,
        "position": 14
    },
    {
        "user": "Garett",
        "input": "ingus",
        "time": {
            "hour": 22,
            "minute": 46,
            "day": 27,
            "month": 1,
            "year": 2025
        },
        "score": 638.4,
        "position": 15
    },
    {
        "user": "Tadeusz",
        "input": "garga",
        "time": {
            "hour": 22,
            "minute": 35,
            "day": 19,
            "month": 1,
            "year": 2025
        },
        "score": 630.32,
        "position": 16
    },
    {
        "user": "Marcin",
        "input": "halkord",
        "time": {
            "hour": 13,
            "minute": 46,
            "day": 6,
            "month": 2,
            "year": 2025
        },
        "score": 626.2,
        "position": 17
    },
    {
        "user": "Marcin",
        "input": "mechazord",
        "time": {
            "hour": 23,
            "minute": 21,
            "day": 4,
            "month": 2,
            "year": 2025
        },
        "score": 625.12,
        "position": 18
    },
    {
        "user": "Marcin",
        "input": "kwakut",
        "time": {
            "hour": 19,
            "minute": 7,
            "day": 2,
            "month": 2,
            "year": 2025
        },
        "score": 621.12,
        "position": 19
    },
    {
        "user": "Marcin",
        "input": "uwkar",
        "time": {
            "hour": 18,
            "minute": 45,
            "day": 1,
            "month": 2,
            "year": 2025
        },
        "score": 617.84,
        "position": 20
    },
    {
        "user": "Marcin",
        "input": "garnel",
        "time": {
            "hour": 0,
            "minute": 4,
            "day": 28,
            "month": 1,
            "year": 2025
        },
        "score": 615.04,
        "position": 21
    },
    {
        "user": "Marcin",
        "input": "wilkus",
        "time": {
            "hour": 0,
            "minute": 10,
            "day": 31,
            "month": 1,
            "year": 2025
        },
        "score": 611.28,
        "position": 22
    },
    {
        "user": "Marcin",
        "input": "burkar",
        "time": {
            "hour": 18,
            "minute": 46,
            "day": 1,
            "month": 2,
            "year": 2025
        },
        "score": 607.76,
        "position": 23
    },
    {
        "user": "Tadeusz",
        "input": "bartok",
        "time": {
            "hour": 21,
            "minute": 26,
            "day": 25,
            "month": 1,
            "year": 2025
        },
        "score": 599.84,
        "position": 24
    },
    {
        "user": "Marcin",
        "input": "ingpal",
        "time": {
            "hour": 19,
            "minute": 51,
            "day": 27,
            "month": 1,
            "year": 2025
        },
        "score": 599.68,
        "position": 25
    },
    {
        "user": "Marcin",
        "input": "karafka",
        "time": {
            "hour": 15,
            "minute": 6,
            "day": 19,
            "month": 1,
            "year": 2025
        },
        "score": 599.12,
        "position": 26
    },
    {
        "user": "Tadeusz",
        "input": "matusz",
        "time": {
            "hour": 21,
            "minute": 13,
            "day": 25,
            "month": 1,
            "year": 2025
        },
        "score": 596.72,
        "position": 27
    },
    {
        "user": "Zefir",
        "input": "webber",
        "time": {
            "hour": 23,
            "minute": 20,
            "day": 17,
            "month": 2,
            "year": 2025
        },
        "score": 594.16,
        "position": 28
    },
    {
        "user": "Marcin",
        "input": "setkve",
        "time": {
            "hour": 18,
            "minute": 41,
            "day": 1,
            "month": 2,
            "year": 2025
        },
        "score": 589.92,
        "position": 29
    },
    {
        "user": "Ing",
        "input": "hutnik",
        "time": {
            "hour": 18,
            "minute": 10,
            "day": 15,
            "month": 2,
            "year": 2025
        },
        "score": 589.44,
        "position": 30
    },
    {
        "user": "Marcin",
        "input": "kwikon",
        "time": {
            "hour": 23,
            "minute": 50,
            "day": 27,
            "month": 1,
            "year": 2025
        },
        "score": 589.04,
        "position": 31
    },
    {
        "user": "Marcin",
        "input": "xurwa",
        "time": {
            "hour": 18,
            "minute": 54,
            "day": 29,
            "month": 1,
            "year": 2025
        },
        "score": 585.6,
        "position": 32
    },
    {
        "user": "Marcin",
        "input": "lubart",
        "time": {
            "hour": 19,
            "minute": 4,
            "day": 4,
            "month": 2,
            "year": 2025
        },
        "score": 584.8,
        "position": 33
    },
    {
        "user": "Marcin",
        "input": "istrak",
        "time": {
            "hour": 12,
            "minute": 26,
            "day": 7,
            "month": 2,
            "year": 2025
        },
        "score": 583.12,
        "position": 34
    },
    {
        "user": "Marcin",
        "input": "gliger",
        "time": {
            "hour": 11,
            "minute": 27,
            "day": 2,
            "month": 2,
            "year": 2025
        },
        "score": 582.96,
        "position": 35
    },
    {
        "user": "Marcin",
        "input": "wijwor",
        "time": {
            "hour": 17,
            "minute": 43,
            "day": 1,
            "month": 2,
            "year": 2025
        },
        "score": 581.44,
        "position": 36
    },
    {
        "user": "Marcin",
        "input": "w\u00f3wald",
        "time": {
            "hour": 9,
            "minute": 40,
            "day": 3,
            "month": 2,
            "year": 2025
        },
        "score": 580.56,
        "position": 37
    },
    {
        "user": "Marcin",
        "input": "psiket",
        "time": {
            "hour": 21,
            "minute": 38,
            "day": 27,
            "month": 1,
            "year": 2025
        },
        "score": 578.56,
        "position": 38
    },
    {
        "user": "Marcin",
        "input": "gurbox",
        "time": {
            "hour": 12,
            "minute": 10,
            "day": 5,
            "month": 2,
            "year": 2025
        },
        "score": 578.56,
        "position": 39
    },
    {
        "user": "Marcin",
        "input": "roklat",
        "time": {
            "hour": 12,
            "minute": 13,
            "day": 5,
            "month": 2,
            "year": 2025
        },
        "score": 578.24,
        "position": 40
    }
    ]




@pytest.mark.parametrize("from_index, to_index, to_index_fixed", [
    (0, 10, 10),
    (0, 40, 30),
    (10, 45, 40),
    ])

def test_check_if_range_is_too_big(mock_leaderboard: Leaderboard, from_index, to_index, to_index_fixed):

    result = mock_leaderboard._check_if_range_is_too_big(from_index, to_index, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    assert result == to_index_fixed




def test_display_leaderboard_default_range(mock_leaderboard: Leaderboard, mock_leaderboard_list):
    
    mock_leaderboard.leaderboard = mock_leaderboard_list


    result = mock_leaderboard.display_leaderboard("", wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    assert len(result) == 10
    
    
    assert result[0] == '1. gurbak - 724.48 (Marcin)'
    assert result[4] == '5. falter - 696.8 (Marcin)'
    assert result[9] == '10. hagen - 670.88 (Ing)'



def test_display_leaderboard_custom_range(mock_leaderboard: Leaderboard, mock_leaderboard_list):
    
    mock_leaderboard.leaderboard = mock_leaderboard_list


    result = mock_leaderboard.display_leaderboard("10 40", wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    assert len(result) == 30
    
    
    assert result[3] == '13. widwan - 647.76 (Marcin)'
    assert result[16] == '26. karafka - 599.12 (Marcin)'
    assert result[21] == '31. kwikon - 589.04 (Marcin)'




# def test_display_leaderboard_spamming(mock_leaderboard: Leaderboard, mock_leaderboard_list):
    
#     mock_leaderboard.leaderboard = mock_leaderboard_list


#     result = mock_leaderboard.display_leaderboard("10 40", wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
#     result2 = mock_leaderboard.display_leaderboard("10 20", wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    
#     assert len(result2) == 0
#     assert len(result) == 30

    



