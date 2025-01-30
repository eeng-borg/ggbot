import pytest
from unittest.mock import patch
from command_modules.korniszon_module.korniszon import score_characters_value, score_vowels_percent, score_repetitions, send_results, score_lenght
import random


class SharedData:
    base_score = 10

# class TestScoreCharactersValue:

#     def test_h(self):
#         assert score_characters_value(0, "h") == 20

#     def test_w(self):
#         assert score_characters_value(0, "w") == 50

#     def test_wh(self):
#         assert score_characters_value(0, "wh") == 35

class TestVowelsPercent:

    @pytest.mark.parametrize("text", ["oooo", "oaauuiióeęą", "aie ou y"])
    def test_100_percent(self, text):
        assert score_vowels_percent(SharedData.base_score, text) == 0

    @pytest.mark.parametrize("text", ["hobo", "dó da"])
    def test_50_percent(self, text):
        assert score_vowels_percent(SharedData.base_score, text) == 14.9

    @pytest.mark.parametrize("text", ["korniszon", "bo b"])
    def test_33_percent(self, text):
        assert score_vowels_percent(SharedData.base_score, text) == 20

    @pytest.mark.parametrize("text", ["bobb", "ccoocccc"])
    def test_25_percent(self, text):
        assert score_vowels_percent(SharedData.base_score, text) == 15.2

    @pytest.mark.parametrize("text", ["kkkkkkk", "ccfdfsffdfgfcccc","dfdf dfdf"])
    def test_0_percent(self, text):
        assert score_vowels_percent(SharedData.base_score, text) == 0

class TestScoreRepetitions:
    
    @pytest.mark.parametrize("text", ["abcd", "oaeąę", "aokjh"])
    def test_single_rep(self, text):
        assert score_repetitions(SharedData.base_score, text) == 10

    @pytest.mark.parametrize("text", ["aabb", "oo", "aabbcc"])
    def test_double_reps(self, text):
        assert score_repetitions(SharedData.base_score, text) == 10

    # for one triple rep, base score is 15 because it's easier to divide it by 1.5 (3 reps/2)
    @pytest.mark.parametrize("text", ["bbb", "fff", "ccc"])    
    def test_triple_rep(self, text):
        assert score_repetitions(15, text) == 10

    @pytest.mark.parametrize("text", ["bbbbc", "ppppo", "ccccg"])
    def test_four_reps(self, text):
        assert score_repetitions(SharedData.base_score, text) == 5
    
    @pytest.mark.parametrize("text", ["bbbcccooo"])
    def test_extra_1(self, text):
        assert round(score_repetitions(SharedData.base_score, text), 2) == 4.44 # round test result to exactly match predicted value

    @pytest.mark.parametrize("text", ["bbbbccdddtttt"])
    def test_extra_2(self, text):
        assert round(score_repetitions(SharedData.base_score, text), 2) == 1.67

class TestScoreLenght:

    @pytest.mark.parametrize("text, result", [
        ("korniszon", 10),
        ("kor", 6.67),
        ("korniszonkorniszon", 4.44),
        ])    
    def test_score_lenght_with_mock(self, text, result):
        with patch("random.randint", return_value = 9):  # Mock random.randint to always return 9        
            
            assert round(score_lenght(SharedData.base_score, text), 2) == result  # Replace with the expected result
            print("Test passed!")

