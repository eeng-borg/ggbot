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

    leaderboard = Leaderboard(mock_driver, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
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
        "user": "Zefir",
        "input": "mavlah",
        "time": "24.02.2025 13:48",
        "score": 742.24,
        "position": 1,
        "timestamp": 1740401280
    },
    {
        "user": "Marcin",
        "input": "gurbak",
        "time": "05.02.2025 12:10",
        "score": 724.48,
        "position": 2,
        "timestamp": 1738753800
    },
    {
        "user": "Zefir",
        "input": "d\u0142ugas",
        "time": "04.02.2025 23:08",
        "score": 706.96,
        "position": 3,
        "timestamp": 1738706880
    },
    {
        "user": "Tadeusz",
        "input": "vigvan",
        "time": "06.02.2025 18:12",
        "score": 706.96,
        "position": 4,
        "timestamp": 1738861920
    },
    {
        "user": "Marcin",
        "input": "waturn",
        "time": "03.02.2025 14:16",
        "score": 698.32,
        "position": 5,
        "timestamp": 1738588560
    },
    {
        "user": "Marcin",
        "input": "falter",
        "time": "31.01.2025 00:12",
        "score": 696.8,
        "position": 6,
        "timestamp": 1738278720
    },
    {
        "user": "Marcin",
        "input": "mator",
        "time": "05.02.2025 11:38",
        "score": 694.68,
        "position": 7,
        "timestamp": 1738751880
    },
    {
        "user": "Tadeusz",
        "input": "halvor",
        "time": "25.01.2025 21:26",
        "score": 677.6,
        "position": 8,
        "timestamp": 1737836760
    },
    {
        "user": "Zefir",
        "input": "gulgot",
        "time": "17.02.2025 21:42",
        "score": 676.16,
        "position": 9,
        "timestamp": 1739824920
    },
    {
        "user": "Ing",
        "input": "jalong",
        "time": "04.02.2025 00:49",
        "score": 675.44,
        "position": 10,
        "timestamp": 1738626540
    },
    {
        "user": "Ing",
        "input": "hagen",
        "time": "19.01.2025 14:27",
        "score": 670.88,
        "position": 11,
        "timestamp": 1737293220
    },
    {
        "user": "Marcin",
        "input": "brudas",
        "time": "02.02.2025 17:32",
        "score": 660.72,
        "position": 12,
        "timestamp": 1738513920
    },
    {
        "user": "Marcin",
        "input": "laptul",
        "time": "29.01.2025 16:01",
        "score": 649.76,
        "position": 13,
        "timestamp": 1738162860
    },
    {
        "user": "Marcin",
        "input": "widwan",
        "time": "04.02.2025 23:39",
        "score": 647.76,
        "position": 14,
        "timestamp": 1738708740
    },
    {
        "user": "Marcin",
        "input": "kurzegatg",
        "time": "04.02.2025 13:27",
        "score": 644.88,
        "position": 15,
        "timestamp": 1738672020
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
        "user": "Garett",
        "input": "ingus",
        "time": "27.01.2025 22:46",
        "score": 638.4,
        "position": 17,
        "timestamp": 1738014360
    },
    {
        "user": "Tadeusz",
        "input": "garga",
        "time": "19.01.2025 22:35",
        "score": 630.32,
        "position": 18,
        "timestamp": 1737322500
    },
    {
        "user": "Marcin",
        "input": "halkord",
        "time": "06.02.2025 13:46",
        "score": 626.2,
        "position": 19,
        "timestamp": 1738845960
    },
    {
        "user": "Marcin",
        "input": "mechazord",
        "time": "04.02.2025 23:21",
        "score": 625.12,
        "position": 20,
        "timestamp": 1738707660
    },
    {
        "user": "Marcin",
        "input": "kwakut",
        "time": "02.02.2025 19:07",
        "score": 621.12,
        "position": 21,
        "timestamp": 1738519620
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
        "user": "Marcin",
        "input": "uwkar",
        "time": "01.02.2025 18:45",
        "score": 617.84,
        "position": 23,
        "timestamp": 1738431900
    },
    {
        "user": "Marcin",
        "input": "garnel",
        "time": "28.01.2025 00:04",
        "score": 615.04,
        "position": 24,
        "timestamp": 1738019040
    },
    {
        "user": "Tadeusz",
        "input": "guffer",
        "time": "21.02.2025 17:55",
        "score": 613.12,
        "position": 25,
        "timestamp": 1740156900
    },
    {
        "user": "Tadeusz",
        "input": "warkon",
        "time": "21.02.2025 18:35",
        "score": 612.48,
        "position": 26,
        "timestamp": 1740159300
    },
    {
        "user": "Marcin",
        "input": "wilkus",
        "time": "31.01.2025 00:10",
        "score": 611.28,
        "position": 27,
        "timestamp": 1738278600
    },
    {
        "user": "Marcin",
        "input": "burkar",
        "time": "01.02.2025 18:46",
        "score": 607.76,
        "position": 28,
        "timestamp": 1738431960
    },
    {
        "user": "Tadeusz",
        "input": "bartok",
        "time": "25.01.2025 21:26",
        "score": 599.84,
        "position": 29,
        "timestamp": 1737836760
    },
    {
        "user": "Marcin",
        "input": "ingpal",
        "time": "27.01.2025 19:51",
        "score": 599.68,
        "position": 30,
        "timestamp": 1738003860
    },
    {
        "user": "Marcin",
        "input": "karafka",
        "time": "19.01.2025 15:06",
        "score": 599.12,
        "position": 31,
        "timestamp": 1737295560
    },
    {
        "user": "Tadeusz",
        "input": "matusz",
        "time": "25.01.2025 21:13",
        "score": 596.72,
        "position": 32,
        "timestamp": 1737835980
    },
    {
        "user": "Zefir",
        "input": "webber",
        "time": "17.02.2025 23:20",
        "score": 594.16,
        "position": 33,
        "timestamp": 1739830800
    },
    {
        "user": "Marcin",
        "input": "setkve",
        "time": "01.02.2025 18:41",
        "score": 589.92,
        "position": 34,
        "timestamp": 1738431660
    },
    {
        "user": "Ing",
        "input": "hutnik",
        "time": "15.02.2025 18:10",
        "score": 589.44,
        "position": 35,
        "timestamp": 1739639400
    },
    {
        "user": "Marcin",
        "input": "kwikon",
        "time": "27.01.2025 23:50",
        "score": 589.04,
        "position": 36,
        "timestamp": 1738018200
    },
    {
        "user": "Marcin",
        "input": "xurwa",
        "time": "29.01.2025 18:54",
        "score": 585.6,
        "position": 37,
        "timestamp": 1738173240
    },
    {
        "user": "Marcin",
        "input": "lubart",
        "time": "04.02.2025 19:04",
        "score": 584.8,
        "position": 38,
        "timestamp": 1738692240
    },
    {
        "user": "Ing",
        "input": "golgos",
        "time": "21.02.2025 18:48",
        "score": 583.68,
        "position": 39,
        "timestamp": 1740160080
    },
    {
        "user": "Marcin",
        "input": "istrak",
        "time": "07.02.2025 12:26",
        "score": 583.12,
        "position": 40,
        "timestamp": 1738927560
    },
    {
        "user": "Marcin",
        "input": "gliger",
        "time": "02.02.2025 11:27",
        "score": 582.96,
        "position": 41,
        "timestamp": 1738492020
    },
    {
        "user": "Zefir",
        "input": "gulgak",
        "time": "18.02.2025 14:51",
        "score": 582.4,
        "position": 42,
        "timestamp": 1739886660
    },
    {
        "user": "Marcin",
        "input": "wijwor",
        "time": "01.02.2025 17:43",
        "score": 581.44,
        "position": 43,
        "timestamp": 1738428180
    },
    {
        "user": "Marcin",
        "input": "w\u00f3wald",
        "time": "03.02.2025 09:40",
        "score": 580.56,
        "position": 44,
        "timestamp": 1738572000
    },
    {
        "user": "Marcin",
        "input": "psiket",
        "time": "27.01.2025 21:38",
        "score": 578.56,
        "position": 45,
        "timestamp": 1738010280
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


    result = mock_leaderboard.display_leaderboard("")
    assert len(result) == 10
    
    
    assert result[0] == '1. mavlah - 742.24 (Zefir)'
    assert result[4] == '5. waturn - 698.32 (Marcin)'
    assert result[9] == '10. jalong - 675.44 (Ing)'



def test_display_leaderboard_custom_range(mock_leaderboard: Leaderboard, mock_leaderboard_list):
    
    mock_leaderboard.leaderboard = mock_leaderboard_list


    result = mock_leaderboard.display_leaderboard("10 40")
    assert len(result) == 30
    
    
    assert result[3] == '13. laptul - 649.76 (Marcin)'
    assert result[16] == '26. warkon - 612.48 (Tadeusz)'
    assert result[21] == '31. karafka - 599.12 (Marcin)'




# def test_display_leaderboard_spamming(mock_leaderboard: Leaderboard, mock_leaderboard_list):
    
#     mock_leaderboard.leaderboard = mock_leaderboard_list


#     result = mock_leaderboard.display_leaderboard("10 40", wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
#     result2 = mock_leaderboard.display_leaderboard("10 20", wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    
#     assert len(result2) == 0
#     assert len(result) == 30

    



