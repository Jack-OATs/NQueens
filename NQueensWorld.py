from random import randint
import numpy as np
from copy import copy


class NQueensWorld:
    def __init__(self, N=5, state=[]):
        self.__N = N
        if state == -1:
            self.state = [randint(0,N-1) for _ in range(N)]
        elif not state:
            self.state = [0 for _ in range(N)]
        else:
            self.__N = len(state)
            if self.is_valid_state(state):
                self.state = state
            else:
                raise ValueError("{} not a valid state for N={}".format(state, N))

    def __str__(self):
        result = ''
        for r in range(self.__N):
            result += "---" * (self.__N) + '-' * (self.__N + 1)
            result += '\n'
            for c in range(self.__N):
                output = '| Q ' if self.state[c] == r else '|   '
                result += output
            result += '|\n'
        result += "---" * (self.__N) + '-' * (self.__N + 1)
        return result

    def __repr__(self):
        return str(self.state)

    def get_N(self):
        return self.__N

    def get_state(self):
        return self.state

    def update_world(self, pos, new_value):
        self.state[pos] = new_value
        if not self.is_valid_state():
            raise ValueError("{} is not a valid state for N={}".format(self.state, self.__N))

    def print_as_matrix(self):
        matrix = [[1 if self.state[c] == r else 0 for c in range(self.__N)] for r in range(self.__N)]
        for line in matrix:
            print(line)

    def get_one_move_next_states(self):
        result = []
        for col in range(self.__N):
            for val in range(self.__N):
                if self.state[col] != val:
                    temp_state = copy(self.state)
                    temp_state[col] = val
                    result.append(temp_state)
        return result

    def is_valid_state(self, state=None):
        if state is None:
            state = self.state
        for item in state:
            if not 0 <= item < self.__N:
                return False
        return True

    def eval_fn(self):
        if not self.is_valid_state():
            raise ValueError("{} is not a valid state for N={}".format(self.state, self.__N))
        matrix = [[1 if self.state[c] == r else 0 for c in range(self.__N)] for r in range(self.__N)]
        matrix = np.array(matrix)
        result = 0
        for c in range(self.__N):
            r = self.state[c]
            directions = [(0, 1), (-1, 1), (1, 1)]
            for direction in directions:
                hits = 0
                temp_r, temp_c = np.add(direction, (r,c))
                while 0 <= temp_r < self.__N and 0 <= temp_c < self.__N:
                    hits += matrix[temp_r, temp_c]
                    temp_r, temp_c = np.add(direction, (temp_r, temp_c))
                result += hits
        return result

    def __eq__(self, other):
        return self.eval_fn() == other.eval_fn()

    def __ne__(self, other):
        return self.eval_fn() != other.eval_fn()

    def __gt__(self, other):
        temp = self.eval_fn() - other.eval_fn()
        return temp < 0

    def __ge__(self, other):
        temp = self.eval_fn() - other.eval_fn()
        return temp <= 0

    def __lt__(self, other):
        temp = self.eval_fn() - other.eval_fn()
        return temp > 0

    def __le__(self, other):
        temp = self.eval_fn() - other.eval_fn()
        return temp >= 0
