import numpy as np


class SemanticNetsAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_sheep, initial_wolves):
        # Add your code here! Your solve method should receive
        # the initial number of sheep and wolves as integers,
        # and return a list of 2-tuples that represent the moves
        # required to get all sheep and wolves from the left
        # side of the river to the right.
        #
        # If it is impossible to move the animals over according
        # to the rules of the problem, return an empty list of
        # moves.
        print(f"solve: {initial_sheep} sheep and {initial_wolves} wolves are on the left bank")
        moves_list = []
        agents_agent = ScorpionAndToad()

        moves_list = agents_agent.real_solve(initial_sheep, initial_wolves)

        return moves_list


class ScorpionAndToad:
    def __init__(self):
        # binary direction value True means next move is right
        self.direction = True
        self.total_players = 0
        ############
        self.all_legal_moves = [(1, 1), (0, 1), (1, 0), (0, 2), (2, 0)]
        # array representing sheep on left, wolves on left, sheep on right, wolves on right
        self.states_history = np.array([[0, 0, 0, 0]])
        # the teams
        self.sheep_left = 0
        self.sheep_right = 0
        self.wolves_left = 0
        self.wolves_right = 0

    def check_move(self, sheep_left, sheep_right, wolves_left, wolves_right):
        if wolves_left > sheep_left > 0:
            return False
        elif wolves_right > sheep_right > 0:
            return False
        elif sheep_left + wolves_left == self.total_players:
            return False
        elif (wolves_right == 1 or sheep_right == 1) and self.direction is False:
            return False
        else:
            return True

    def state_check(self, sheep_left, sheep_right, wolves_left, wolves_right):
        new_move = np.array([[sheep_left, sheep_right, wolves_left, wolves_right]])
        states_copy = np.copy(self.states_history)
        new_states = np.vstack(states_copy, new_move)
        unique_moves = np.unique(new_states, axis=0)
        if np.equal(new_states, unique_moves).all():
            return True, new_states
        else:
            return False, states_copy

    def next_move(self, mov, sheep_left, sheep_right, wolves_left, wolves_right, direction, history):
        #, direction, history
        #
        non_d_sheep_mov, non_d_wolf_mov = mov
        if direction:
            sheep_left -= non_d_sheep_mov
            sheep_right += non_d_sheep_mov
            wolves_left -= non_d_wolf_mov
            wolves_right += non_d_wolf_mov
        else:
            sheep_left += non_d_sheep_mov
            sheep_right -= non_d_sheep_mov
            wolves_left += non_d_wolf_mov
            wolves_right -= non_d_wolf_mov
        #########
        # check #
        #########
        st_check_, st_hist = self.state_check(sheep_left, sheep_right, wolves_left, wolves_right)
        mov_check_ = self.check_move(sheep_left, sheep_right, wolves_left, wolves_right)
        if st_check_ and mov_check_ and sheep_left >= 0 and sheep_right >= 0 and wolves_left >= 0 and wolves_right >= 0:
            return True, st_hist
        elif st_check_ and mov_check_:
            print("not enough sheep or wolves")
            print("stop here")
            return True, st_hist
        else:
            return False, history

    def terminal(self, direction, now_state):
        # if the boat needs to go left and total characters on left side of river are < 1, answer is found
        sheep_left, sheep_right, wolves_left, wolves_right = now_state[-1:]
        if not direction and (sheep_left + wolves_left) < 1:
            return True
        elif sheep_left < 0 or sheep_right < 0 or wolves_left < 0 or wolves_right < 0:
            return True
        else:
            return False

    def go_right(self, sheep_left, sheep_right, wolves_left, wolves_right
                 , now_state, terminal_check, depth_check, a, b):
        #
        term = self.terminal(True, now_state)
        if term or depth_check <= 0:
            return tuple()
        #
        default_a = float("-inf")
        default_tuple = np.random.choice(np.array(self.all_legal_moves))
        test_depth = depth_check
        #
        for rm in self.all_legal_moves:
            if test_depth > 0:
                test_depth -= 1
                #
                valid_mov, new_his = self.next_move(rm, sheep_left, sheep_right, wolves_left, wolves_right, True, now_state)
                #
                if valid_mov:
                    right_term = self.terminal(False, new_his)
                    left_score, left_move = self.go_left(self, sheep_left, sheep_right, wolves_left, wolves_right
                                                         , new_his, right_term, test_depth, a, b)
                    #
                    if left_score > default_a:
                        default_a, default_tuple = left_score, left_move
                        a = max(a, default_a)
                    #
                    if default_a >= b:
                        return (default_a, )

        return rm

    def go_left(self, sheep_left, sheep_right, wolves_left, wolves_right
                 , now_state, terminal_check, depth_check, a, b):
        #
        term = self.terminal(True, now_state)
        if term or depth_check <= 0:
            return tuple()
        #
        default_a = float("-inf")
        default_tuple = np.random.choice(np.array(self.all_legal_moves))
        test_depth = depth_check
        #
        for rm in self.all_legal_moves:
            test_depth -= 1
            valid_mov, new_his = self.next_move(rm, sheep_left, sheep_right, wolves_left, wolves_right, True, now_state)

        return False

    def a_b(self, depth, a, b):
        # Add your code here! Your solve method should receive
        # the initial number of sheep and wolves as integers,
        # and return a list of 2-tuples that represent the moves
        # required to get all sheep and wolves from the left
        # side of the river to the right.
        #
        # If it is impossible to move the animals over according
        # to the rules of the problem, return an empty list of
        # moves.
        next_tuple = np.random.choice(np.array(self.all_legal_moves))
        #
        #next_tuple = self.go_right(self.states_history, False, depth, a, b)
        if self.direction:
            next_tuple = self.go_right(self.sheep_left, self.sheep_right, self.wolves_left, self.wolves_right,
                                       self.states_history, self.direction, depth, a, b)
        else:
            next_tuple = self.go_left(self.sheep_left, self.sheep_right, self.wolves_left, self.wolves_right,
                                       self.states_history, self.direction, depth, a, b)
        print("algo got the next move to be ", next_tuple)
        non_d_sheep_mov, non_d_wolf_mov = next_tuple
        #
        if self.direction:
            self.sheep_left -= non_d_sheep_mov
            self.sheep_right += non_d_sheep_mov
            self.wolves_left -= non_d_wolf_mov
            self.wolves_right += non_d_wolf_mov
        else:
            self.sheep_left += non_d_sheep_mov
            self.sheep_right -= non_d_sheep_mov
            self.wolves_left += non_d_wolf_mov
            self.wolves_right -= non_d_wolf_mov
        ###########
        # updates #
        ###########
        self.direction = not self.direction
        new_state = np.array([[self.sheep_left, self.sheep_right, self.wolves_left, self.wolves_right]])
        self.states_history = np.vstack(self.states_history, new_state)
        #
        return next_tuple

    def real_solve(self, initial_sheep, initial_wolves):
        moves_list = []
        #
        self.total_players = initial_sheep + initial_wolves
        self.states_history[0, 0] = initial_sheep
        self.states_history[0, 1] = initial_wolves
        self.sheep_left = initial_sheep
        self.wolves_left = initial_wolves
        #
        depth = 0
        if initial_sheep >= 10:
            depth = initial_wolves + initial_sheep + 5
        else:
            depth = 10 * initial_sheep
        #
        while self.sheep_left + self.wolves_left > 0:
            a, b = float("-inf"), float("inf")
            next_move = self.a_b(depth, a, b)
            moves_list.append(next_move)

        return moves_list
