"""
Tic Tac Toe Player
"""

import math
import copy
import sys

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
    Specification:
    The player function should take a board state as input, and return which player’s turn it is (either X or O).
    In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
    Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    """

    # algorithm: count Xs and Os on board to see whose turn it is next

    moveCountX = 0
    moveCountO = 0
    for row in board:
        for cell in row:
            if (cell == X):
                moveCountX += 1
            elif (cell == O):
                moveCountO += 1

    if (moveCountX > moveCountO):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Specification:
    The actions function should return a set of all of the possible actions that can be taken on a given board.
    Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2)
    and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    Possible moves are any cells on the board that do not already have an X or an O in them.
    Any return value is acceptable if a terminal board is provided as input.
    """

    # set of possible actions, each action represented as a tuple (int row_index, int col_index)
    possibleActions = set()

    for row_index in range(3):
        for cell_index in range(3):
            if (board[row_index][cell_index] == EMPTY):
                possibleActions.add((row_index,cell_index))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Specification:
    The result function takes a board and an action as input, and should return a new board state,
    without modifying the original board.
    If action is not a valid action for the board, your program should raise an exception.
    The returned board state should be the board that would result from taking the original input board,
    and letting the player whose turn it is make their move at the cell indicated by the input action.
    Importantly, the original board should be left unmodified: since Minimax will ultimately require
    considering many different board states during its computation. This means that simply updating
    a cell in board itself is not a correct implementation of the result function. You’ll likely want to
    make a deep copy of the board first before making any changes.
    """

    # first check action is valid
    if (board[action[0]][action[1]] != EMPTY):
        raise Exception(f"Invalid action: {action} on board: {board}")

    active_player = player(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = active_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Specification:
    The winner function should accept a board as input, and return the winner of the board if there is one.
    If the X player has won the game, your function should return X.
    If the O player has won the game, your function should return O.
    One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    You may assume that there will be at most one winner (that is, no board will ever have both players
    with three-in-a-row, since that would be an invalid board state).
    If there is no winner of the game (either because the game is in progress, or because it ended in a tie),
    the function should return None.
    """
    if ( row_winner(board[0],X) or
         row_winner(board[1],X) or
         row_winner(board[2],X) or
         col_winner(board,0,X) or
         col_winner(board,1,X) or
         col_winner(board,2,X) or
         tlbr_diag_winner(board,X) or
         trbl_diag_winner(board,X) ):
        return X
    elif ( row_winner(board[0],O) or
           row_winner(board[1],O) or
           row_winner(board[2],O) or
           col_winner(board,0,O) or
           col_winner(board,1,O) or
           col_winner(board,2,O) or
           tlbr_diag_winner(board,O) or
           trbl_diag_winner(board,O) ):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    Specification:
    The terminal function should accept a board as input, and return a boolean value indicating whether the game is over.
    If the game is over, either because someone has won the game or because all cells have been filled without
    anyone winning, the function should return True.
    Otherwise, the function should return False if the game is still in progress.
    """
    if (winner(board) != None):
        return True
    else:
        return board_full(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Specification:
    The utility function should accept a terminal board as input and output the utility of the board.
    If X has won the game, the utility is 1. If O has won the game, the utility is -1.
    If the game has ended in a tie, the utility is 0.
    You may assume utility will only be called on a board if terminal(board) is True.
    """
    winning_player = winner(board)
    if (winning_player == X):
        return 1
    elif (winning_player == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Specification:
    The minimax function should take a board as input, and return the optimal move for the player to move on that board.
    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.
    If multiple moves are equally optimal, any of those moves is acceptable.
    If the board is a terminal board, the minimax function should return None.
    """
    if (terminal(board)):
        return None

    active_player = player(board)
    optimal_action = None
    alpha = -sys.maxsize - 1
    beta = sys.maxsize

    # print("-------------------------------------")
    # print(f"minimax: for player: {active_player}")
    # print_board(board)

    if (active_player == X):
        # maximising player
        optimal_score = -sys.maxsize - 1
        #print(f"Looking for move with highest min score...")
        for action in actions(board):
            score = min_value(result(board, action), alpha, beta)
            #print(f"X Move ({action[0]},{action[1]}) gives max_value: {score}")
            if (score > optimal_score):
                optimal_score = score
                optimal_action = action
                #print(f"BEST SCORE SO FAR! - ({action[0]},{action[1]})")
            alpha = max(alpha,score)
            if beta <= alpha:
                # alpha / beta pruning
                break
        #print(f"Choosing best move - ({optimal_action[0]},{optimal_action[1]})")
        return optimal_action
    else:
        # minimising player
        optimal_score = sys.maxsize
        # print(f"Looking for move with lowest max score...")
        for action in actions(board):
            score = max_value(result(board, action), alpha, beta)
            # print(f"O Move ({action[0]},{action[1]}) gives max_value: {score}")
            if (score < optimal_score):
                optimal_score = score
                optimal_action = action
                # print(f"BEST SCORE SO FAR! - ({action[0]},{action[1]})")
            beta = min(beta,score)
            if beta <= alpha:
                # alpha / beta pruning
                break
        # print(f"Choosing best move - ({optimal_action[0]},{optimal_action[1]})")
        return optimal_action

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    score = -sys.maxsize -1
    for action in actions(board):
        score = max(score, min_value(result(board, action), alpha, beta))
        alpha = max(alpha,score)
        if beta <= alpha:
            # alpha / beta pruning
            break
    return score

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    score = sys.maxsize
    for action in actions(board):
        score = min(score, max_value(result(board, action), alpha, beta))
        beta = min(beta,score)
        if beta <= alpha:
            # alpha / beta pruning
            break
    return score

def board_full(board):
    for row in board:
        for cell in row:
            if (cell == EMPTY):
                return False

    return True

def row_winner(row, player):
    """
    Return true if the player has won by placing 3 moves into the row
    """
    return ( row[0] == player and
             row[1] == player and
             row[2] == player )

def col_winner(board, col_index, player):
    """
    Return true if the player has won by placing 3 moves into column (col_index) of the board
    """
    return ( board[0][col_index] == player and
             board[1][col_index] == player and
             board[2][col_index] == player )

def tlbr_diag_winner(board, player):
    """
    Return true if the player has won by placing 3 moves into the topleft to bottomright diagonal of the board
    """
    return ( board[0][0] == player and
             board[1][1] == player and
             board[2][2] == player )

def trbl_diag_winner(board, player):
    """
    Return true if the player has won by placing 3 moves into the topright to bottomleft diagonal of the board
    """
    return ( board[0][2] == player and
             board[1][1] == player and
             board[2][0] == player )

def print_board(board):
    print(f" {player_token(board[0][0])} | {player_token(board[0][1])} | {player_token(board[0][2])} ")
    print(f"---+---+---")
    print(f" {player_token(board[1][0])} | {player_token(board[1][1])} | {player_token(board[1][2])} ")
    print(f"---+---+---")
    print(f" {player_token(board[2][0])} | {player_token(board[2][1])} | {player_token(board[2][2])} ")

def player_token(player):
    if (player == X):
        return 'X'
    elif (player == O):
        return 'O'
    else:
        return ' '


