import pytest
from selenium import webdriver
from utils.types import CommandData
from command_modules.korniszon_module.korniszon import Korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from users import Cooldown
from sql_database import Database


def dummy_wait_find_input_and_send_keys(*args, **kwargs):
    return

@pytest.fixture
def mock_leaderboard():
    database = Database()
    leaderboard = Leaderboard(database=database, wait_find_input_and_send_keys=dummy_wait_find_input_and_send_keys)
    return leaderboard



@pytest.fixture
def mock_korniszon(mock_leaderboard):
    database = Database()
    korniszon = Korniszon(database=database, leaderboard=mock_leaderboard)

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

def test_get_range_from_input(input, result, mock_leaderboard: Leaderboard):

    _result = mock_leaderboard._get_range_from_input(input)
    assert _result == result




@pytest.mark.parametrize("limit, result", [
    (1, 1),
    (10, 10),
    (45, 30),
    (31, 30),
    ])

def test_check_if_range_is_too_big(mock_leaderboard: Leaderboard, limit, result):

    actual_result = mock_leaderboard._check_if_range_not_too_big(limit)
    assert actual_result == result




def test_display_leaderboard_default_range(mock_leaderboard: Leaderboard):
    
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

    



