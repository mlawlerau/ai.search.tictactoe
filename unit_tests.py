import unittest
from tictactoe import X, O, EMPTY, initial_state, player, actions, result, winner, terminal, utility, minimax

class TestTicTacToe(unittest.TestCase):

    #
    # Player
    # The player function should take a board state as input, and return which player’s turn it is (either X or O).
    #

    def test_player_initial(self):
        """In the initial game state, X gets the first move."""
        board = initial_state()
        self.assertEqual(player(board), X)

    def test_player_o(self):
        """Subsequently, the player alternates with each additional move."""
        board = initial_state()
        board[0][0] = X
        self.assertEqual(player(board), O)

    def test_player_x(self):
        """Subsequently, the player alternates with each additional move."""
        board = initial_state()
        board[0][0] = X
        board[0][1] = O
        self.assertEqual(player(board), X)

    #
    # Actions
    # The actions function should return a set of all of the possible actions that can be taken on a given board.
    #

    def test_actions_initial(self):
        """Return a set of all of the possible actions that can be taken on a given board."""
        board = initial_state()
        all_actions = [ (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2) ]
        self.assertIsInstance(actions(board), set)
        self.assertEqual(list(actions(board)).sort(), all_actions.sort())

    def test_actions_midgame(self):
        """Return a set of all of the possible actions that can be taken on a given board."""
        board = [[X, O, EMPTY],
                 [O, EMPTY, X],
                 [X, EMPTY, O]]
        possible_actions = [ (0,2), (1,1), (2,1) ]
        self.assertIsInstance(actions(board), set)
        self.assertEqual(list(actions(board)).sort(), possible_actions.sort())

    #
    # Result
    # The result function takes a board and an action as input, and should return a new board state,
    # without modifying the original board.
    #

    def test_result_invalid_action(self):
        """If action is not a valid action for the board, your program should raise an exception."""
        board = [[X, O, EMPTY],
                 [O, EMPTY, X],
                 [X, EMPTY, O]]
        invalid_action = (0,0)
        try:
            result(board,invalid_action)
        except Exception:
            pass
        else:
            self.fail('Exception not raised for invalid action')

    def test_result_normal_path(self):
        """The returned board state should be the board that would result from taking the original input board,
        and letting the player whose turn it is make their move at the cell indicated by the input action.."""
        board_0 = initial_state()
        first_move_x = (0,0)
        board_1 = result(board_0, first_move_x)
        self.assertEqual(board_1[0][0], X)
        second_move_o = (1,1)
        board_2 = result(board_1, second_move_o)
        self.assertEqual(board_2[0][0], X)
        self.assertEqual(board_2[1][1], O)
        third_move_x = (0,1)
        board_3 = result(board_2, third_move_x)
        self.assertEqual(board_3[0][0], X)
        self.assertEqual(board_3[1][1], O)
        self.assertEqual(board_3[0][1], X)
        fourth_move_x = (2,2)
        board_4 = result(board_3, fourth_move_x)
        self.assertEqual(board_4[0][0], X)
        self.assertEqual(board_4[1][1], O)
        self.assertEqual(board_4[0][1], X)
        self.assertEqual(board_4[2][2], O)
        """Importantly, the original board should be left unmodified"""
        self.assertEqual(board_0, initial_state())

    #
    # Winner
    # The winner function should accept a board as input, and return the winner of the board if there is one.
    #

    def test_winner_none_in_progress(self):
        """If there is no winner of the game (either because the game is in progress, or because it ended in a tie),
        the function should return None."""
        board = [[X, O, EMPTY],
                 [O, EMPTY, X],
                 [X, EMPTY, O]]
        self.assertEqual(winner(board), None)

    def test_winner_none_tie(self):
        """If there is no winner of the game (either because the game is in progress, or because it ended in a tie),
        the function should return None."""
        board = [[X, O, X],
                 [O, O, X],
                 [X, X, O]]
        self.assertEqual(winner(board), None)

    def test_winner_x(self):
        """If the X player has won the game, your function should return X."""
        board = [[X, O, X],
                 [O, O, X],
                 [O, X, X]]
        self.assertEqual(winner(board), X)

    def test_winner_o(self):
        """If the O player has won the game, your function should return O."""
        board = [[X, X, O],
                 [EMPTY, O, X],
                 [O, EMPTY, EMPTY]]
        self.assertEqual(winner(board), O)

    def test_winner_three_in_a_row_x(self):
        """One can win the game with three of their moves in a row horizontally, vertically, or diagonally."""
        board = [[X, X, X],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board), X)
        board = [[EMPTY, EMPTY, EMPTY],
                 [X, X, X],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board), X)
        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [X, X, X]]
        self.assertEqual(winner(board), X)
        board = [[X, EMPTY, EMPTY],
                 [X, EMPTY, EMPTY],
                 [X, EMPTY, EMPTY]]
        self.assertEqual(winner(board), X)
        board = [[EMPTY, X, EMPTY],
                 [EMPTY, X, EMPTY],
                 [EMPTY, X, EMPTY]]
        self.assertEqual(winner(board), X)
        board = [[EMPTY, EMPTY, X],
                 [EMPTY, EMPTY, X],
                 [EMPTY, EMPTY, X]]
        self.assertEqual(winner(board), X)
        board = [[EMPTY, EMPTY, X],
                 [EMPTY, X, EMPTY],
                 [X, EMPTY, EMPTY]]
        self.assertEqual(winner(board), X)
        board = [[X, EMPTY, EMPTY],
                 [EMPTY, X, EMPTY],
                 [EMPTY, EMPTY, X]]
        self.assertEqual(winner(board), X)

    def test_winner_three_in_a_row_o(self):
        """One can win the game with three of their moves in a row horizontally, vertically, or diagonally."""
        board = [[O, O, O],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board), O)
        board = [[EMPTY, EMPTY, EMPTY],
                 [O, O, O],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board), O)
        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [O, O, O]]
        self.assertEqual(winner(board), O)
        board = [[O, EMPTY, EMPTY],
                 [O, EMPTY, EMPTY],
                 [O, EMPTY, EMPTY]]
        self.assertEqual(winner(board), O)
        board = [[EMPTY, O, EMPTY],
                 [EMPTY, O, EMPTY],
                 [EMPTY, O, EMPTY]]
        self.assertEqual(winner(board), O)
        board = [[EMPTY, EMPTY, O],
                 [EMPTY, EMPTY, O],
                 [EMPTY, EMPTY, O]]
        self.assertEqual(winner(board), O)
        board = [[EMPTY, EMPTY, O],
                 [EMPTY, O, EMPTY],
                 [O, EMPTY, EMPTY]]
        self.assertEqual(winner(board), O)
        board = [[O, EMPTY, EMPTY],
                 [EMPTY, O, EMPTY],
                 [EMPTY, EMPTY, O]]
        self.assertEqual(winner(board), O)

    #
    # Terminal
    # The terminal function should accept a board as input, and return a boolean value indicating
    # whether the game is over.
    #

    def test_terminal_initial(self):
        """the function should return False if the game is still in progress."""
        board = initial_state()
        self.assertEqual(terminal(board), False)

    def test_terminal_midgame(self):
        """the function should return False if the game is still in progress."""
        board = [[X, O, EMPTY],
                 [O, EMPTY, X],
                 [X, EMPTY, O]]
        self.assertEqual(terminal(board), False)

    def test_terminal_game_wone(self):
        """If the game is over, because someone has won the game, the function should return True."""
        board = [[X, O, X],
                 [O, O, X],
                 [O, X, X]]
        self.assertEqual(terminal(board), True)

    def test_terminal_board_full(self):
        """If the game is over, because all cells have been filled without anyone winning, the function should return True."""
        board = [[X, O, X],
                 [O, O, X],
                 [X, X, O]]
        self.assertEqual(terminal(board), True)

    #
    # Utility
    # The utility function should accept a terminal board as input and output the utility of the board.
    #

    def test_utility_winner_x(self):
        """If X has won the game, the utility is 1."""
        board = [[X, O, X],
                 [O, O, X],
                 [O, X, X]]
        self.assertEqual(utility(board), 1)

    def test_utility_winner_o(self):
        """If O has won the game, the utility is -1."""
        board = [[X, X, O],
                 [EMPTY, O, X],
                 [O, EMPTY, EMPTY]]
        self.assertEqual(utility(board), -1)

    def test_utility_tie(self):
        """If the game has ended in a tie, the utility is 0."""
        board = [[X, O, X],
                 [O, O, X],
                 [X, X, O]]
        self.assertEqual(utility(board), 0)

    #
    # Minimax
    # The minimax function should take a board as input, and return the
    # optimal move for the player to move on that board.
    #

    def test_minimax_terminal_board_full(self):
        """If the board is a terminal board, the minimax function should return None."""
        board = [[X, O, X],
                 [O, O, X],
                 [X, X, O]]
        self.assertEqual(minimax(board), None)

    def test_minimax_terminal_game_won(self):
        """If the board is a terminal board, the minimax function should return None."""
        board = [[X, O, X],
                 [O, O, X],
                 [O, X, X]]
        self.assertEqual(minimax(board), None)

    def test_minimax_take_immediate_win(self):
        """The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.
        If multiple moves are equally optimal, any of those moves is acceptable."""
        board = [[X, X, EMPTY],
                 [O, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(minimax(board), (0,2))

    def test_minimax_choose_from_two_wins(self):
        """The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.
        If multiple moves are equally optimal, any of those moves is acceptable."""
        board = [[X, O, X],
                 [O, X, O],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertIn(minimax(board), [ (2,0), (2,2)])

    def test_minimax_prevent_immediate_loss(self):
        """The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.
        If multiple moves are equally optimal, any of those moves is acceptable."""
        board = [[O, X, EMPTY],
                 [EMPTY, X, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(minimax(board), (2,1))

if __name__ == '__main__':
    unittest.main()