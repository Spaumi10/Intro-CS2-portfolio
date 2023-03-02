# Author: Michael Spaulding
# GitHub username: Spaumi10
# Date: 03/01/2023
# Description: Program that replicates a checkers game with multiple classes and
# methods.


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
        # TODO look into refactoring some of this code below into other methods.
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

            if self._board.get_board()[ending_row][ending_column]:
                raise InvalidDestination

            # Get piece object that needs moved.
            piece_to_move = self._board.get_board()[starting_row][starting_column]

            # Checks if current player moved other player's piece.
            if piece_to_move.get_piece_color() != self._players_turn:
                raise InvalidSquare

            # Move piece
            self._board.get_board()[ending_row][ending_column] = piece_to_move

            # Checking if move took piece, removing piece, and adding to captured pieces.
            self.capture_pieces(
                starting_row, ending_row, starting_column, ending_column, other_player
            )

            # Revert starting_square to None.
            self._board.get_board()[starting_row][starting_column] = None

            # This is how I am handling do they have an extra jump.
            # additional_move_response = input(
            #     "Do you have an another jump? (y/n): "
            # ).lower()
            # if additional_move_response != "y":
            #     additional_move = False

            # Checks if piece should be kinged or triple kinged.
            self.king_check(current_player, piece_to_move, ending_row)

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

    # TODO test king_check(). Tested, and passed, by brute force, not during actual game.
    def king_check(self, player_obj, piece_obj, ending_row):
        """
        Checks if piece should be made a king or triple king and, if so,
        modifies piece object and add piece type to player object..
        """
        # Check for making White or Black to king.
        if piece_obj.get_piece_type() == "Black" and ending_row == 0:
            piece_obj.set_piece_type("Black_king")
            player_obj.add_king()

        elif piece_obj.get_piece_type() == "White" and ending_row == 7:
            piece_obj.set_piece_type("White_king")
            player_obj.add_king()

        # Check for making White_king or Black_king to triple king.
        elif piece_obj.get_piece_type() == "Black_king" and ending_row == 7:
            piece_obj.set_piece_type("Black_Triple_King")
            player_obj.remove_king()
            player_obj.add_triple_king()

        elif piece_obj.get_piece_type() == "White_king" and ending_row == 0:
            piece_obj.set_piece_type("White_Triple_king")
            player_obj.remove_king()
            player_obj.add_triple_king()

    def capture_pieces(
        self, starting_row, ending_row, starting_column, ending_column, other_player
    ):
        """Calculates number of pieces captured and returns quantity of pieces."""
        # For moves going up and right.
        if starting_row > ending_row and starting_column < ending_column:
            row_coordinates = [num for num in range(ending_row + 1, starting_row)]
            column_coordinates = [
                num for num in range(ending_column - 1, starting_column, -1)
            ]

        # For moves going up and left.
        elif starting_row > ending_row and starting_column > ending_column:
            row_coordinates = [num for num in range(ending_row + 1, starting_row)]
            column_coordinates = [
                num for num in range(ending_column + 1, starting_column)
            ]

        # For moves going down and right.
        elif starting_row < ending_row and starting_column < ending_column:
            row_coordinates = [num for num in range(ending_row - 1, starting_row, -1)]
            column_coordinates = [
                num for num in range(ending_column - 1, starting_column, -1)
            ]

        # For moves going down and left.
        elif starting_row < ending_row and starting_column > ending_column:
            row_coordinates = [num for num in range(ending_row - 1, starting_row, -1)]
            column_coordinates = [
                num for num in range(ending_column + 1, starting_column)
            ]

        # Obtain coordinates of squares that were jumpped.
        coordinates = zip(row_coordinates, column_coordinates)
        captured_pieces = 0
        # Searches jumped squares for opponent pieces and removes if present.
        for coordinate in coordinates:
            current_square = self._board.get_board()[coordinate[0]][coordinate[1]]
            if current_square:
                if "triple" in current_square.get_piece_type():
                    current_square.remove_triple_king()
                elif "king" in current_square.get_piece_type():
                    current_square.remove_king()

                self._board.get_board()[coordinate[0]][coordinate[1]] = None
                captured_pieces += 1
                other_player.add_captured_piece(1)
                # A triple king can take 2 pieces at most. This stops the search
                # for additional squares that may have been jumped, but there
                # can't be additional opponent pieces (this assumes the player
                # is following this rule, which seemed to be indicated in Ed
                # discussion by professor.)
                if captured_pieces == 2:
                    break

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

    def __init__(self, player_name, piece_color):
        self._player_name = player_name
        self._piece_color = piece_color
        self._king_count = 0
        self._triple_king_count = 0
        self._captured_pieces_count = 0

    def get_piece_color(self):
        """Returns piece color."""
        return self._piece_color

    def get_player_name(self):
        """Returns player name."""
        return self._player_name

    def add_king(self):
        """Adds a king to player's pieces."""
        self._king_count += 1

    def remove_king(self):
        """Removes a king from player's pieces."""
        self._king_count -= 1

    def get_king_count(self):
        """Returns the number of king pieces that the player has."""
        return self._king_count

    def add_triple_king(self):
        """Adds a triple king to player's pieces."""
        self._triple_king_count += 1

    def remove_triple_king(self):
        """Removes a triple king from player's pieces."""
        self._triple_king_count -= 1

    def get_triple_king_count(self):
        """Returns the number of triple king pieces that the player has."""
        return self._triple_king_count

    def add_captured_piece(self, quantity):
        """Adds captured piece to count."""
        self._captured_pieces_count += quantity

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

    def get_piece_type(self):
        """Returns piece type."""
        return self._piece_type

    def set_piece_type(self, new_piece_type):
        """Sets piece to piece_type."""
        self._piece_type = new_piece_type

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


class InvalidDestination(Exception):
    """"""

    def __str__(self):
        return "Your destination is on top of a current piece. Not valid."


game = Checkers()

Player1 = game.create_player("Adam", "White")

Player2 = game.create_player("Lucy", "Black")


game.play_game("Lucy", (5, 4), (4, 3))


game.play_game("Adam", (2, 1), (3, 2))

print("\n")
for row in game._board.get_board():
    print(row)

game.play_game("Lucy", (4, 3), (3, 2))


# game.play_game("Adam", (2, 7), (3, 6))


# game.play_game("Lucy", (5, 6), (4, 5))


# game.play_game("Adam", (3, 6), (5, 4))


# game.play_game("Lucy", (6, 5), (4, 3))


# game.play_game("Adam", (2, 3), (3, 4))


# game.play_game("Lucy", (5, 0), (4, 1))


# game.play_game("Adam", (1, 2), (2, 3))

# game.play_game("Lucy", (2, 1), (0, 0))

# game.play_game("Adam", (3, 4), (7, 1))

# game.play_game("Lucy", (0, 0), (7, 7))

# game.play_game("Adam", (7, 1), (0, 0))
# print("\n")
# for row in game._board.get_board():
#     print(row)

# print(game.get_checker_details((0, 1)))

# print(Player1.get_captured_pieces_count())
