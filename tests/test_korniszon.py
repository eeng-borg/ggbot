import pytest
from unittest.mock import patch
from selenium import webdriver
from utils.types import CommandData
from command_modules.korniszon_module.korniszon import Korniszon
from command_modules.korniszon_module.leaderboard import Leaderboard
from users import Cooldown


class SharedData:
    base_score = 10

@pytest.fixture(scope="module")
def mock_korniszon() -> Korniszon:

    driver = webdriver.Chrome()
    leaderboard = Leaderboard()
    korniszon = Korniszon(driver, leaderboard)

    return korniszon


@pytest.mark.parametrize("text, result", [
("oooo", 0),
("oaauuiióeęą", 0),
("aie ou y", 0),
("hobo", 14.9),
("dó da", 14.9),
("korniszon", 20),
("bo b", 20),
("bobb", 15.2),
("ccoocccc", 15.2),
("kkkkkkk", 0),
("fdf dfdf", 0)
])
def test_vowels_percent(text, result, mock_korniszon: Korniszon):
    assert mock_korniszon.score_vowels_percent(SharedData.base_score, text) == result



@pytest.mark.parametrize("text, result", [
("abcd", 10),
("aokjh", 10),
("aabb", 10),
("oo", 10),
("bbbbc", 5),
("ccccg", 5),
("bbbcccooo", 4.44),
("bbbbccdddtttt", 1.67)
])
def test_repetitions(text, result, mock_korniszon: Korniszon):
    assert mock_korniszon.score_repetitions(SharedData.base_score, text) == result


@pytest.mark.parametrize("text, result", [
    ("korniszon", 10),
    ("kor", 6.67),
    ("korniszonkorniszon", 4.44),
    ])    
def test_score_lenght(text, result, mock_korniszon: Korniszon):
    with patch("random.randint", return_value = 9):  # Mock random.randint to always return 9        
        
        assert round(mock_korniszon.score_lenght(SharedData.base_score, text), 2) == result  # Replace with the expected result
        print("Test passed!")



class TestCooldown:
        
    @pytest.fixture(scope='class')
    def mock_driver(self):

        driver = webdriver.Chrome()
        return driver
    
    @pytest.fixture(scope='class')
    def mock_leaderboard(self) -> Leaderboard:

        leaderboard = Leaderboard()
        return leaderboard 


    @pytest.fixture(scope='class')
    def mock_korniszon(self, mock_driver, mock_leaderboard):

        korniszon = Korniszon(mock_driver, mock_leaderboard)

        Cooldown('Maciek')
        Cooldown('Janusz')

        return korniszon  
    
    
    @pytest.fixture(scope='class')
    def mock_command_data(self):

        data = CommandData(user='Janusz', input='bualoa', command='korniszon', time={'day':1,'month':2,'year':2000,'hour':1,'minute':2})
        return data
    
    
    def dummy_send_results(*args, **kwargs):
        # Return a controlled value instead of triggering a timeout.
        return  # or a list of dummy elements if needed
    
    @staticmethod
    def dummy_exceptions(mock_command_data: CommandData, mock_leaderboard: Leaderboard):

        return

        # # in case if korniszon is already on leaderborad
        # if any(mock_command_data['input'] == entry["input"] for entry in mock_leaderboard.leaderboard):

        #     pozycja = mock_leaderboard.get_position(mock_command_data['input'])
        #     return f"{mock_command_data['input']} już jest na pozycji {pozycja}. Wymyśl nowego korniszona <okok>"
        

        # # in case there were no letters in korniszon and you were left with empty variable
        # if len(mock_command_data['input']) == 0:

        #     return "3456 punktów <zniesmaczony>. Naum się w korniszony!"
        

        # elif len(mock_command_data['input']) > 30:

        #     return "Nie będę oceniał takiego długasa <nono>"
        
    @staticmethod
    def dummy_cooldown_wait_responde(*args, **kwargs):
        # time_left = cooldown.time_remaining()
        # return f"Poczekaj {time_left} sekund, {korniszon_data['user']} <luzik>"
        return 'Czekaj'

    

    @pytest.fixture
    def patched_korniszon(self, monkeypatch: pytest.MonkeyPatch, mock_leaderboard, mock_driver):

        monkeypatch.setattr(Korniszon, 'send_results', self.dummy_send_results)
        monkeypatch.setattr(Korniszon, 'exceptions', TestCooldown.dummy_exceptions)
        monkeypatch.setattr(Korniszon, 'cooldown_wait_responde', TestCooldown.dummy_cooldown_wait_responde)

        return Korniszon(mock_driver, mock_leaderboard)
    

    def test_adding(self, mock_command_data, mock_leaderboard: Leaderboard, patched_korniszon: Korniszon):

        cooldown = Cooldown.find_user(mock_command_data['user'])
        patched_korniszon.rate_korniszon(mock_command_data, cooldown)

        assert len(mock_leaderboard.leaderboard) == 1


    def test_adding_too_fast(self, mock_command_data, mock_leaderboard: Leaderboard, patched_korniszon: Korniszon):

        cooldown = Cooldown.find_user(mock_command_data['user'])
        patched_korniszon.rate_korniszon(mock_command_data, cooldown)
        cooldown.start()
        patched_korniszon.rate_korniszon(mock_command_data, cooldown)

        assert len(mock_leaderboard.leaderboard) == 1




