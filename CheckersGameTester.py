import unittest

import CheckersGame


class TestCreatePlayer(unittest.TestCase):
    """"""

    def test_players_list(self):
        """"""
        game = CheckersGame.Checkers()
        game.create_player("Milo", "Black")
        game.create_player("Otis", "White")
        player_names_list = [
            player_obj.get_player_name() for player_obj in game.get_players()
        ]
        self.assertEqual(player_names_list, ["Milo", "Otis"])


unittest.main()
