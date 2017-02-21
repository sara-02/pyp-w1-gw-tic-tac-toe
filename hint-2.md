# Hint 2 - Check for a winner

### Is a winning combination

The `_is_winning_combination(board, combination, player)` is rather simple. Let's take another look at our board:

```
(0,0) | (0,1) | (0,2)
---------------------
(1,0) | (1,1) | (1,2)
---------------------
(2,0) | (2,1) | (2,2)
```

The first row "combination" is expressed as: `[(0,0), (0,1), (0,2)]`. If we have the same player in every position that's a potential winning combination. For example, if all the positions are taken by the player `'X'`, then the following call should return `True`:

```python
first_row = [(0,0), (0,1), (0,2)]
_is_winning_combination(board, first_row, 'X')  # True
```

The implementaton of the function is simple. We just need to make sure that the given player is the **ONLY** player present at any of those positions:

```python
def _is_winning_combination(board, combination, player):
    for position in combination:
        # If we any position DOESN'T contain a player
        # we can just return False
        if board[position[0]][position[1]] != player:
            return False
    return True
```

### Check winning combinations

We're using the `_check_winning_combinations(board, player)` function in our `move` function to check if the game has a winner. This is simple, we just need to check every possible combination for a winner. What are the possible winning combinations? Simple: 3 rows, 3 columns and the two diagonals:


```python
def _check_winning_combinations(board, player):
    combinations = (
        # horizontals
        ((0,0), (0,1), (0,2)),
        ((1,0), (1,1), (1,2)),
        ((2,0), (2,1), (2,2)),

        # verticals
        ((0,0), (1,0), (2,0)),
        ((0,1), (1,1), (2,1)),
        ((0,2), (1,2), (2,2)),

        # diagonals
        ((0,0), (1,1), (2,2)),
        ((2,0), (1,1), (0,2)),
    )
    for combination in combinations:
        if _is_winning_combination(board, combination, player):
            return player
    return None
```
