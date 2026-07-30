"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    if x_count == o_count:
        return X
    else:
        return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                possible.add((i, j))

    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise ValueError("Invalid action")

    new_board = copy.deepcopy(board)

    i, j = action

    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    lines = []

    # Add rows
    for row in board:
        lines.append(row)

    # Add columns
    for col in range(3):
        lines.append([
            board[0][col],
            board[1][col],
            board[2][col]
        ])

    # Add diagonals
    lines.append([
        board[0][0],
        board[1][1],
        board[2][2]
    ])

    lines.append([
        board[0][2],
        board[1][1],
        board[2][0]
    ])

    # Check each line
    for line in lines:
        if line == [X, X, X]:
            return X
        if line == [O, O, O]:
            return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Someone has won
    if winner(board) is not None:
        return True

    # Any empty squares?
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False

    # No empty squares and no winner
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    w = winner(board)

    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0
    


def max_value(board):
    """
    Returns the maximum utility value for X.
    """

    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v
    

def min_value(board):
    """
    Returns the minimum utility value for O.
    """

    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If game is over, no move
    if terminal(board):
        return None

    # X wants to maximize
    if player(board) == X:

        best_value = -math.inf
        best_action = None

        for action in actions(board):
            value = min_value(result(board, action))

            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    # O wants to minimize
    else:

        best_value = math.inf
        best_action = None

        for action in actions(board):
            value = max_value(result(board, action))

            if value < best_value:
                best_value = value
                best_action = action

        return best_action