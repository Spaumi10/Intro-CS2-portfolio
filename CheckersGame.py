class Checkers:
    """
    Represents a checkers game, including board and gameplay.
    """

    def __init__(self):
        self._BLACK_CHECKERS = 12
        self._WHITE_CHECKERS = 12

    def create_player(self, player_name, piece_color):
        """Returns a player object with name and piece color."""
        # TODO check on whether the parameter name should be piece_color or checker_color. Seems to be conflict between what is mentioned here and for the Player class constructor.
        return Player(player_name, piece_color)

    def play_game(
        self, player_name, starting_square_location, destination_square_location
    ):
        """
        Moves the player's piece from the starting location to the destination
        location.
        """

    def get_checker_details(self, square_location):
        """Returns the checker deatils present at the square_location."""

    def print_board(self):
        """
        Prints the current checker board, with placement of current pieces,
        None for empty spaces.
        """

    def game_winner(self):
        """
        Returns the name of the winning player, or if game not over, returns
        that fact.
        """


class Player:
    """
    Represents a checkers player.
    """

    def __init__(self, player_name, checker_color):
        self._player_name = player_name
        self._checker_color = checker_color

    def get_king_count(self):
        """Returns the number of king pieces that the player has."""

    def get_triple_king_count(self):
        """Returns the number of triple king pieces that the player has."""

    def get_captured_pieces_count(self):
        """Returns the number of opponent peces that the player has captured."""
