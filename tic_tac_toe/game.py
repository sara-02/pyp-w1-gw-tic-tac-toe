from tic_tac_toe.exceptions import GameOver, InvalidMovement

# internal helpers


def _position_is_empty_in_board(position, board):
    """
    Checks if given position is empty ("-") in the board.

    :param position: Two-elements tuple representing a
                     position in the board. Example: (0, 1)
    :param board: Game board.

    Returns True if given position is empty, False otherwise.
    """
    if board[position[0]][position[1]] == '-':
        return True
    return False


def _position_is_valid(position):
    """
    Checks if given position is a valid. To consider a position as valid, it
    must be a two-elements tuple, containing values from 0 to 2.
    Examples of valid positions: (0,0), (1,0)
    Examples of invalid positions: (0,0,1), (9,8), False

    :param position: Two-elements tuple representing a
                     position in the board. Example: (0, 1)

    Returns True if given position is valid, False otherwise.
    """
    valid_positions = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
    ]

    for p in valid_positions:
        if position == p:
            return True

    return False


def _board_is_full(board):
    """
    Returns True if all positions in given board are occupied.

    :param board: Game board.
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                return False

    return True


def _is_winning_combination(board, combination, player):
    """
    Checks if all 3 positions in given combination are occupied by given player.

    :param board: Game board.
    :param combination: Tuple containing three position elements.
                        Example: ((0,0), (0,1), (0,2))

    Returns True of all three positions in the combination belongs to given
    player, False otherwise.
    """
    for position in combination:
        if board[position[0]][position[1]] != player:
            return False
    return True


def _check_winning_combinations(board, player):
    """
    There are 8 posible combinations (3 horizontals, 3, verticals and 2 diagonals)
    to win the Tic-tac-toe game.
    This helper loops through all these combinations and checks if any of them
    belongs to the given player.

    :param board: Game board.
    :param player: One of the two playing players.

    Returns the player (winner) of any of the winning combinations is completed
    by given player, or None otherwise.
    """
    # check for 1st diagonal
    if _is_winning_combination(board, ((0, 0), (1, 1), (2, 2)), player):
        return player

    # check for 2nd diagonal
    elif _is_winning_combination(board, ((0, 2), (1, 1), (2, 0)), player):
        return player

    # check horizontally:
    elif _is_winning_combination(board, ((0, 0), (0, 1), (0, 2)), player):
        return player
    elif _is_winning_combination(board, ((1, 0), (1, 1), (1, 2)), player):
        return player
    elif _is_winning_combination(board, ((2, 0), (2, 1), (2, 2)), player):
        return player

    # check vertically
    elif _is_winning_combination(board, ((0, 0), (1, 0), (2, 0)), player):
        return player
    elif _is_winning_combination(board, ((0, 1), (1, 1), (2, 1)), player):
        return player
    elif _is_winning_combination(board, ((0, 2), (1, 2), (2, 2)), player):
        return player

    return None
# public interface


def start_new_game(player1, player2):
    """
    Creates and returns a new game configuration.
    """
    return {'player1': player1,
            'player2': player2,
            'board': [
                ["-", "-", "-"],
                ["-", "-", "-"],
                ["-", "-", "-"],
            ],
            'next_turn': player1,
            'winner': None
            }


def get_winner(game):
    """
    Returns the winner player if any, or None otherwise.
    """
    return game['winner']


def move(game, player, position):
    """
    Performs a player movement in the game. Must ensure all the pre requisites
    checks before the actual movement is done.
    After registering the movement it must check if the game is over.
    """
    board = game['board']
    if _board_is_full(board) or game['winner']:
        raise InvalidMovement("Game is over.")
    if get_next_turn(game) == player:
        if _position_is_valid(position):
            if _position_is_empty_in_board(position, board):
                board[position[0]][position[1]] = player
                winner = _check_winning_combinations(board, player)
                if winner:
                    game['winner'] = player
                    game['next_turn'] = None
                    raise GameOver("\"{0}\" wins!".format(player))
                elif _board_is_full(board):
                    raise GameOver("Game is tied!")
                else:
                    game['next_turn'] = game['player2'] if player == game[
                        'player1'] else game['player1']
            else:
                raise InvalidMovement("Position already taken.")
        else:
            raise InvalidMovement("Position out of range.")
    else:
        raise InvalidMovement("\"{0}\" moves next.".format(game['next_turn']))


def get_board_as_string(game):
    """
    Returns a string representation of the game board in the current state.
    """

    board = game['board']

    s = "\n"
    for i in range(3):
        for j in range(3):
            s = s + board[i][j]
            if j == 0 or j == 1:
                s = s + "  |  "
        if i == 0 or i == 1:
            s = s + "\n--------------\n"
    s = s + "\n"
    return s


def get_next_turn(game):
    """
    Returns the player who plays next, or None if the game is already over.
    """
    if _board_is_full(game['board']) or game['winner'] is not None:
        return None
    return game['next_turn']
