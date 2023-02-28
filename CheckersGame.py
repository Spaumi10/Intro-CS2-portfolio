# Author: Michael Spaulding
# GitHub username: Spaumi10
# Date: 02/25/2023
# Description:


class Checkers:
    """
    Represents a checkers game, including board and gameplay.

    Attributes:
    - board is a Board object for game with starting pieces in place
    - players is a list of player objects
    - players_turn keeps track of who's turn it is.
    """

    BLACK_CHECKERS = 12
    WHITE_CHECKERS = 12

    def __init__(self):
        self._board = Board()
        self._players = []
        self._players_turn = "Black"

    def create_player(self, player_name, piece_color):
        """Returns a player object with name and piece color."""
        # TODO check on whether the parameter name should be piece_color or checker_color. Seems to be conflict between what is mentioned here and for the Player class constructor.
        created_player = Player(player_name, piece_color)
        self._players.append(created_player)
        return created_player

    def play_game(
        self, player_name, starting_square_location, destination_square_location
    ):
        """
        Moves the player's piece from the starting location to the destination
        location.
        """

        # Gets current and non-current player object and collects current player name to check below.
        current_player_names = []
        for player_obj in self._players:
            current_player_names.append(player_obj.get_player_name())
            if player_obj.get_piece_color() == self._players_turn:
                current_player = player_obj
            else:
                other_player = player_obj

        # Checks if passed player_name is a current player.
        if player_name not in current_player_names:
            raise InvalidPlayer

        # Checks if correct player made move
        if player_name != current_player.get_player_name():
            raise OutofTurn
        else:
            starting_row = starting_square_location[0]
            starting_column = starting_square_location[1]
            ending_row = destination_square_location[0]
            ending_column = destination_square_location[1]

            # Get piece object that needs moved.
            piece_to_move = self._board.get_board()[starting_row][starting_column]

            # Checks if current player moved other player's piece.
            if piece_to_move.get_piece_color() != self._players_turn:
                raise InvalidSquare

            # Move piece
            self._board.get_board()[ending_row][ending_column] = piece_to_move

            # Revert starting_square to None.
            self._board.get_board()[starting_row][starting_column] = None

            # TODO Account for additional jumps by current_player, before switching to next player.

            # Moves turn to next player.
            if self._players_turn == "Black":
                self._players_turn = "White"
            else:
                self._players_turn = "Black"

            return other_player.get_captured_pieces_count()

    def get_checker_details(self, square_location):
        """Returns the checker details present at the square_location."""
        row = square_location[0]
        column = square_location[1]
        try:
            if self._board.get_board()[row][column]:
                return self._board.get_board()[row][column]
            else:
                return None
        except IndexError:
            raise InvalidSquare

    def print_board(self):
        """
        Prints the current checker board, with placement of current pieces,
        None for empty spaces.
        """
        print(self._board.get_board())

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
        self._king_count = 0
        self._triple_king_count = 0
        self._captured_pieces_count = 0

    def get_piece_color(self):
        """Returns piece color."""
        return self._checker_color

    def get_player_name(self):
        """Returns player name."""
        return self._player_name

    def get_king_count(self):
        """Returns the number of king pieces that the player has."""
        return self._king_count

    def get_triple_king_count(self):
        """Returns the number of triple king pieces that the player has."""
        return self._triple_king_count

    def get_captured_pieces_count(self):
        """Returns the number of opponent peces that the player has captured."""
        return self._captured_pieces_count


class Board:
    """Creates game board with starting pieces in place."""

    def __init__(self):
        self._board = []
        # TODO Shorten code for creating a board w/ pieces.
        # Creates board and places starting pieces.
        for i in range(8):
            temp_list = []
            for i in range(8):
                # White piece placement
                # Places white pieces on 1st and 3rd row from top.
                if len(self._board) % 2 == 0 and len(self._board) < 3:
                    if len(temp_list) % 2 == 1:
                        temp_list.append(Piece("White", "White"))
                    else:
                        temp_list.append(None)
                # Places white pieces on 2nd row from top.
                elif len(self._board) % 2 == 1 and len(self._board) < 3:
                    if len(temp_list) % 2 == 0:
                        temp_list.append(Piece("White", "White"))
                    else:
                        temp_list.append(None)

                # Black piece placement
                # Places black pieces on 6th and 8th row from top.
                elif len(self._board) % 2 == 0 and len(self._board) > 4:
                    if len(temp_list) % 2 == 1:
                        temp_list.append(Piece("Black", "Black"))
                    else:
                        temp_list.append(None)
                # Places black pieces on 7th row from top.
                elif len(self._board) % 2 == 1 and len(self._board) > 4:
                    if len(temp_list) % 2 == 0:
                        temp_list.append(Piece("Black", "Black"))
                    else:
                        temp_list.append(None)

                # Fills in empty spaces
                else:
                    temp_list.append(None)

            self._board.append(temp_list)

    def get_board(self):
        """Returns board."""
        return self._board


class Piece:
    """Represents a checkers piece"""

    def __init__(self, piece_color, piece_type):
        self._piece_color = piece_color
        self._piece_type = piece_type

    def check_moves(self, starting_square_location, destination_square_location):
        """Checks if move available for piece type."""
        # TODO Not finished with checking moves.
        # King piece moves
        if self._piece_type == "king":
            pass

        # Triple king piece moves
        elif self._piece_type == "triple_king":
            pass

        # Regular piece moves
        else:
            pass

    def get_piece_color(self):
        """Returns piece's color."""
        return self._piece_color

    def set_piece_type(self, piece_type):
        """Sets piece to piece_type."""
        self._piece_type = piece_type

    def __str__(self) -> str:
        return self._piece_type

    def __repr__(self) -> str:
        return self._piece_type


# Exceptions
class OutofTurn(Exception):
    """"""

    def __str__(self):
        return "It is not your turn."


class InvalidSquare(Exception):
    """"""

    def __str__(self):
        return "Your move would take you off the board or you picked a piece that is not yours."

    pass


class InvalidPlayer(Exception):
    """"""

    def __str__(self):
        return "That name is not a current player of this game."


game = Checkers()

for row in game._board.get_board():
    print(row)

Player1 = game.create_player("Adam", "White")

Player2 = game.create_player("Lucy", "Black")


game.play_game("Lucy", (5, 6), (4, 7))

game.play_game("Adam", (2, 1), (3, 0))


# print("\n")
# for row in game._board.get_board():
#     print(row)


# print(game.get_checker_details((0, 1)))

# Player1.get_captured_pieces_count()
