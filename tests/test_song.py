import unittest
from func_sugg import song2


class TestSongFunction(unittest.TestCase):
    def test_song(self):
        # given
        # essentially monophonic patterns
        patterns = [
            [
                {"pitch": 60, "duration": 0.5},
                {"pitch": 67, "duration": 0.5}
            ],
            [
                {"pitch": 64, "duration": 0.5},
                {"pitch": 62, "duration": 0.5}
            ]
        ]
        # when
        # i'm not sure about this state thing
        song_func = song2(patterns)

        # then
        print(song_func())
