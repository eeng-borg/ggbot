import pytest
from unittest.mock import patch
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




class TestAdding:
        
   
    @pytest.fixture(scope = 'class')
    def mock_driver(self):

        driver = webdriver.Chrome()
        return driver
    
    @pytest.fixture
    def mock_leaderboard(self):

        leaderboard = Leaderboard()
        return leaderboard


    @pytest.fixture
    def mock_korniszon(self, mock_driver, mock_leaderboard):

        korniszon = Korniszon(mock_driver, mock_leaderboard)

        return korniszon  
    
    
    @pytest.fixture(scope='class')
    def mock_command_data(self):

        data = CommandData(user='Janusz', input='bualoa', command='korniszon', time={'day':1,'month':2,'year':2000,'hour':1,'minute':2})
        return data
    
    
    def dummy_send_results(*args, **kwargs):
        # Return a controlled value instead of triggering a timeout.
        return []  # or a list of dummy elements if needed

    

    def test_adding_new(self, mock_korniszon: Korniszon, mock_command_data, monkeypatch, mock_leaderboard):

        monkeypatch.setattr(mock_korniszon, 'send_results', self.dummy_send_results)

        cooldown = Cooldown.find_user(mock_command_data['user'])
        mock_korniszon.rate_korniszon(mock_command_data, cooldown)

        assert len(mock_leaderboard.leaderboard) == 1


    def test_adding_new2(self, mock_korniszon: Korniszon, mock_command_data, monkeypatch, mock_leaderboard):

        monkeypatch.setattr(mock_korniszon, 'send_results', self.dummy_send_results)

        cooldown = Cooldown.find_user(mock_command_data['user'])
        mock_korniszon.rate_korniszon(mock_command_data, cooldown)

        assert len(mock_leaderboard.leaderboard) == 1
