# Author: Michael Spaulding
# GitHub username: Spaumi10
# Date: 03/06/2023
# Description: Unittests for CheckersGame.

import unittest

import CheckersGame


class TestCheckers(unittest.TestCase):
    """Tests the Checkers class."""

    def test_players_list(self):
        """
        Tests whether a player that was added is actually in the player names list.
        """
        game = CheckersGame.Checkers()
        player1 = game.create_player("Milo", "Black")
        player2 = game.create_player("Otis", "White")
        player_names_list = [
            player_obj.get_player_name() for player_obj in game.get_players()
        ]
        self.assertIn("Milo", player_names_list)

    def test_play_game_invalidplayer(self):
        """
        Tests whether an exception is raised when a non-player tries to make a move.
        """
        game = CheckersGame.Checkers()
        player1 = game.create_player("Romeo", "Black")
        player2 = game.create_player("Juliet", "White")
        game.play_game("Romeo", (5, 0), (4, 1))
        game.play_game("Juliet", (2, 3), (3, 2))

        self.assertRaises(
            CheckersGame.InvalidPlayer, game.play_game, "Beatrice", (5, 6), (4, 7)
        )

    def test_king_check(self):
        """Tests whether a kinged pieced is correctly applied."""
        game = CheckersGame.Checkers()
        player1 = game.create_player("Cleopatra", "Black")
        player2 = game.create_player("Dido", "White")
        game.play_game("Cleopatra", (5, 0), (4, 1))
        game.play_game("Dido", (2, 1), (3, 2))
        game.play_game("Cleopatra", (4, 1), (3, 0))
        game.play_game("Dido", (2, 3), (3, 4))
        game.play_game("Cleopatra", (5, 6), (4, 7))
        game.play_game("Dido", (1, 2), (2, 3))
        game.play_game("Cleopatra", (3, 0), (2, 1))
        game.play_game("Dido", (0, 3), (1, 2))
        game.play_game("Cleopatra", (2, 1), (0, 3))
        self.assertEqual(1, player1.get_king_count())

    def test_outofturn(self):
        """Tests whether exception is raised when a player plays out of turn."""
        game = CheckersGame.Checkers()
        player1 = game.create_player("Cleopatra", "Black")
        player2 = game.create_player("Dido", "White")
        game.play_game("Cleopatra", (5, 0), (4, 1))
        game.play_game("Dido", (2, 1), (3, 2))
        game.play_game("Cleopatra", (4, 1), (3, 0))
        game.play_game("Dido", (1, 2), (2, 1))
        game.play_game("Cleopatra", (3, 0), (1, 2))
        # game.play_game("Cleopatra", (6, 1), (5, 0))
        self.assertRaises(
            CheckersGame.OutofTurn, game.play_game, "Cleopatra", (6, 1), (5, 0)
        )


class TestBoard(unittest.TestCase):
    """Tests the Board class, through the Checkers class."""

    def test_get_board(self):
        """Makes sure board isn't blank."""
        board = CheckersGame.Board()
        game_board = board.get_board()
        blank_game_board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]

        self.assertNotEqual(blank_game_board, game_board)


unittest.main()
