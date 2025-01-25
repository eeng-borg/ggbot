import pytest
from unittest.mock import patch
from command_modules.korniszon_module.leaderboard import Leaderboard


leaderboard = Leaderboard()

class TestGetUserStats:

    @pytest.mark.parametrize(["user", "result"], [
        ("", 0),
        ("Aku", 4),
        ("Garond", 3),
        ("Bombel", 0)
        ])
    def test_score_sum(self, user, result):
        assert leaderboard.leaderboard___get_user_korniszons(self, user, 1) == result

    # @pytest.mark.parametrize("text", ["oooo", "oaauuiióeęą", "aie ou y"])
    # def test_100_percent(self, text):
    #     assert score_vowels_percent(SharedData.base_score, text) == 0
