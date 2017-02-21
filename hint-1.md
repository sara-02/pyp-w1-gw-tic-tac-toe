# Hint 1

The first thing to figure out about this project is the _public interface_ of our code. Those functions that will be used directly by the user (_user_ in this context is another programmer working with **our** code).

### Start New Game

In this case everything starts with the `start_new_game` function. Our user has complete access to the details of this implementation, as you can see in [this test](https://github.com/rmotr-group-projects/pyp-w1-gw-tic-tac-toe/blob/master/tests/test_main.py#L20). Here's the implementation:

```python
def start_new_game(player1, player2):
    """
    Creates and returns a new game configuration.
    """
    return {
        'player1': player1,
        'player2': player2,
        'board': [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"],
        ],
        'next_turn': player1,
        'winner': None
    }
```

### Get Winner

The winner comes directly from the `game` object we've created with `start_new_game`:

```python
def get_winner(game):
    """
    Returns the winner player if any, or None otherwise.
    """
    return game['winner']
```

### Move

This is probably the most important function in the game. We've taken the "divide and conquer" approach for this particular function. We've splitted the whole _"move"_ functionality in many different functions. So `move` is just a mashup of smaller independent functions working together. Here's an annotated working version of `move`:

```python

def move(game, player, position):
    board = game['board']
    # If the game already has a winner of the board is full
    # there's nothing else to see. We raise an InvalidMovement exception
    # We rely on _board_is_full here.
    if game['winner'] or _board_is_full(board):
        raise InvalidMovement('Game is over.')
    
    # If the player attempting to make the move is not
    # the allowed one, we raise another exception.
    # We use get_next_turn here.
    if player != get_next_turn(game):
        raise InvalidMovement('"{}" moves next.'.format(game['next_turn']))
    
    # If the position that the user is trying to move is not valid
    # we raise another exception.
    # We rely on the _position_is_valid function
    if not _position_is_valid(position):
        raise InvalidMovement('Position out of range.')
    
    # If the position is already full (someone perform a previous
    # move on that position) we raise another exception.
    # We use the _position_is_empty_in_board function.
    if not _position_is_empty_in_board(position, board):
        raise InvalidMovement('Position already taken.')
        
    # IMPORTANT POINT
    # Up to this point we've checked all the ILEGAL moves.
    # From now on everything else is valid.
    
    # The first thing we do is we make the actual move.
    # We mark the position with the player.
    board[position[0]][position[1]] = player
    
    # We then check to see if that last move, made
    # some player to win.
    winner = _check_winning_combinations(board, player)
    
    # If the movement resulted in a winner we do some
    # bookeeping tasks.
    # If we didn't produce a winner, but we filled the whole board
    # we raise the GameOver exception with a "tied game".
    # Or in any other case (final _else_), we just
    # swap the next player to keep the game going.
    if winner:
        game['winner'] = winner
        game['next_turn'] = None
        raise GameOver('"{}" wins!'.format(winner))
    elif _board_is_full(board):
        game['next_turn'] = None
        raise GameOver('Game is tied!'.format(winner))
    else:
        game['next_turn'] = game['player1'] if game['next_turn'] == game['player2'] else game['player2']
```
