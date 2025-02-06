import pytest
from unittest.mock import patch
from command_modules.korniszon_module.korniszon import Korniszon
from selenium import webdriver
from command_modules.korniszon_module.leaderboard import Leaderboard


class SharedData:
    base_score = 10

@pytest.fixture(scope="module")
def mock_korniszon():

    driver = webdriver.Chrome()
    leaderboard = Leaderboard()
    korniszon = Korniszon(driver, leaderboard)
    return korniszon



        # @pytest.mark.parametrize("text, result", [
        # ("korniszon", 10),
        # ("kor", 6.67),
        # ("korniszonkorniszon", 4.44),
        # ])  

    # @pytest.mark.parametrize("text", ["oooo", "oaauuiióeęą", "aie ou y"])

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
def test_vowels_percent(text, result, mock_korniszon):
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
def test_repetitions(text, result, mock_korniszon):
    assert mock_korniszon.score_repetitions(SharedData.base_score, text) == result


@pytest.mark.parametrize("text, result", [
    ("korniszon", 10),
    ("kor", 6.67),
    ("korniszonkorniszon", 4.44),
    ])    
def test_score_lenght(text, result, mock_korniszon):
    with patch("random.randint", return_value = 9):  # Mock random.randint to always return 9        
        
        assert round(mock_korniszon.score_lenght(SharedData.base_score, text), 2) == result  # Replace with the expected result
        print("Test passed!")

