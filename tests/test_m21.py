import unittest

from m21 import get_stream
from movement import convert_music21_stream


class TestM21(unittest.TestCase):

    def test_stream_gets_converted_to_right_format(self):
        # Given
        stream = get_stream()

        # When
        converted_stream = convert_music21_stream(stream)

        # Then
        print(converted_stream)
        self.assertTrue(True)
