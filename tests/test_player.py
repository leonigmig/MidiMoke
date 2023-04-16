import unittest

from player import Player


class TestPlayer(unittest.TestCase):
    def testPlayer(self):
        with self.assertRaises(ValueError):
            player = Player(None, None)
            player.play = False
