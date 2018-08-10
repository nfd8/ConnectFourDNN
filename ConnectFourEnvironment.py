import gym
import csv
import random
import numpy as np
import copy


class ConnectFourEnv(gym.Env):

    def __init__(self, board=np.zeros([6,7], dtype=int)):
        """
        Reads the input file specified to initialize the environment
        :param input_file: A .txt file specifying all relevant environment parameters
        """
        self.game_state = GameState(board=board)
        self.game_over = False


    def step(self, game_state=None, action=None):
        ...

    def reset(self):
        """
        Resets the environment state with random alert. If fresh is True then experts will all be
        available and attacker will have maximum budget. If False then these are randomized.
        :param fresh: Whether or not agents' resources should be set to their full capacity
        :param start_state: Specifies a specific state from which to start the environment
        """
        ...

    def rand_state(self, fresh=False):
        """
        Returns a random state without modifying the environments internal variables
        :param fresh: If fresh=True, all agents start with maximum resources available
        :return: A random GameState object
        """
        ...


class GameState:
    @property
    def player_turn(self):
        return self._player_turn

    @property
    def num_checkers(self):
        return (self.board > 0).sum(axis=0)

    def __init__(self, board=np.zeros([6, 7], dtype=int), turn=1):
        assert(board.shape == (6, 7) and type(board) == np.ndarray)
        self.board = board
        self._player_turn = turn

    def step(self, action):
        assert(action >= 0 or action <= 6)
        next_board = copy.copy(self.board)
        next_board[(next_board.shape[0] - 1) - self.num_checkers[action], action] = self.player_turn
        next_state = GameState(board=next_board, turn=self.next_turn())
        game_over = self.win_condition()
        if game_over:
            reward = 100
        else:
            reward = 0
        return next_state, reward, game_over

    def win_condition(self):
        player = self.player_turn
        # Horizontal Win
        for row in reversed(range(self.board.shape[0])):
            horz_window = np.array([0, 1, 2, 3])
            for _ in range((self.board.shape[1] - 4) + 1):
                # Check if player owns all 4 positions in window
                owned = 0
                for i in range(4):
                    if self.board[row, horz_window[i]] == player:
                        owned += 1
                    else:
                        break
                if owned == 4:
                    return True
                horz_window += 1
        # Vertical Win
        for col in reversed(range(self.board.shape[1])):
            vert_window = np.array([5, 4, 3, 2])
            for _ in range((self.board.shape[0] - 4) + 1):
                # Check if player owns all 4 position in window
                owned = 0
                for i in range(4):
                    if self.board[vert_window[i], col] == player:
                        owned += 1
                    else:
                        break
                if owned == 4:
                    return True
                vert_window -= 1
        # Forward Slash Win
        for col in range((self.board.shape[1] - 4) + 1):
            fslash_window = np.array([5, 4, 3, 2])
            col_list = np.array([col, col+1, col+2, col+3])
            for _ in range((self.board.shape[0] - 4) + 1):
                # Check if player owns all 4 positions in window
                owned = 0
                for i in range(4):
                    if self.board[fslash_window[i], col_list[i]] == player:
                        owned += 1
                    else:
                        break
                    if owned == 4:
                        return True
                fslash_window -= 1
        # Backward Slash Win
        for col in range((self.board.shape[1] - 4) + 1):
            bslash_window = np.array([2, 3, 4, 5])
            col_list = np.array([col, col+1, col+2, col+3])
            for _ in range((self.board.shape[0] - 4) + 1):
                # Check if player owns all 4 positions in window
                owned = 0
                for i in range(4):
                    if self.board[bslash_window[i], col_list[i]] == player:
                        owned += 1
                    else:
                        break
                    if owned == 4:
                        return True
                bslash_window -= 1
        return False

    @player_turn.setter
    def player_turn(self, value):
        if value == 1 or value == 2:
            self._player_turn = value
        else:
            raise ValueError("player_turn must be 1 or 2.")

    def next_turn(self):
        if self.player_turn == 1:
            return 2
        elif self.player_turn == 2:
            return 1



test_board = np.array([[0, 0, 0, 1, 2, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [1, 1, 2, 1, 2, 1, 1]])
gs = GameState()
while not gs.win_condition():
    print(gs.board)
    gs, _, _ = gs.step(random.randint(0, 6))
    print('\n\n')
print('dink')