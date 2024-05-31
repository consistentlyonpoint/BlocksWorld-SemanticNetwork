import numpy as np
import heapq


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

    def path_cost_(self, history):
        r, c = history.shape()
        return r

    def check_move(self, sheep_left, sheep_right, wolves_left, wolves_right, direction):
        print("sheepLeft: ", sheep_left)
        print("sheepRight: ", sheep_right)
        print("wolvesLeft: ", wolves_left)
        print("wolvesRight: ", wolves_right)
        if (wolves_left > sheep_left) and (sheep_left > 0):
            return False
        elif (wolves_right > sheep_right) and (sheep_right > 0):
            return False
        elif sheep_left + wolves_left == self.total_players:
            return False
        elif (wolves_right + sheep_right == 1) and direction is False:
            return False
        elif sheep_left < 0 or sheep_right < 0 or wolves_left < 0 or wolves_right < 0:
            return False
        else:
            return True

    def state_check_REAL(self, sheep_left, sheep_right, wolves_left, wolves_right):
        new_move = np.array([[sheep_left, sheep_right, wolves_left, wolves_right]])
        states_copy = np.copy(self.states_history)
        new_states = np.vstack((states_copy, new_move))
        unique_moves = np.unique(new_states, axis=0)
        if np.equal(new_states, unique_moves).all():
            return True, new_states
        else:
            return False, states_copy

    def state_check(self, sheep_left, sheep_right, wolves_left, wolves_right, st_hist):
        new_move = np.array([[sheep_left, sheep_right, wolves_left, wolves_right]])
        states_copy = np.copy(st_hist)
        new_states = np.vstack((states_copy, new_move))
        unique_moves = np.unique(new_states, axis=0)
        #
        print("in state_check")
        print("old history")
        print(st_hist)
        #print("\n")
        print("new stack")
        print(new_states)
        #print("\n")
        print("unique?")
        print(unique_moves)
        #
        #if np.equal(new_states, unique_moves).all():
        if new_states.shape == unique_moves.shape:
            return True, new_states
        else:
            return False, states_copy

    def next_move(self, mov, sheep_left, sheep_right, wolves_left, wolves_right, direction, history):
        print("the mov was: ", mov)
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
        print("check the check_move")
        mov_check_ = self.check_move(sheep_left, sheep_right, wolves_left, wolves_right, not direction)
        print("mov_check_ was: ", mov_check_)
        if mov_check_:
            print("check the state_check")
            st_check_, st_hist = self.state_check(sheep_left, sheep_right, wolves_left, wolves_right, history)
            print("state_check was: ", st_check_)
            if st_check_:
                return True, st_hist
                #elif st_check_ and mov_check_:
                #    print("not enough sheep or wolves")
                #    print("stop here")
                #    return True, st_hist
        #    else:
        #        return False, history
        #else:
        #    return False, history
        return False, history

    def terminal(self, direction, now_state):
        #print("history3")
        #print(now_state)
        #print(now_state.shape)
        #print(now_state[-1:])
        #print(now_state[-1][:])
        # if the boat needs to go left and total characters on left side of river are < 1, answer is found
        #sheep_left, sheep_right, wolves_left, wolves_right = now_state[-1:]
        sheep_left, sheep_right, wolves_left, wolves_right = now_state[-1][:]
        if not direction and (sheep_left + wolves_left) < 1:
            return True
        elif sheep_left < 0 or sheep_right < 0 or wolves_left < 0 or wolves_right < 0:
            return True
        else:
            return False

    def go_right(self, sheep_left, sheep_right, wolves_left, wolves_right, now_state, mvs, depth_check):
        #
        #print("history")
        #print(now_state)
        #print(now_state.shape)
        #print(now_state[-1:])
        #
        # if not direction and (sheep_left + wolves_left) < 1:
        #     return True
        # elif sheep_left < 0 or sheep_right < 0 or wolves_left < 0 or wolves_right < 0:
        #     return True
        # else:
        #     return False
        #
        term = self.terminal(True, now_state)
        if term or depth_check <= 0:
            return tuple()
        #
        #default_a = float("-inf")
        #default_tuple = np.random.choice(np.array(self.all_legal_moves))
        test_depth = depth_check
        test_list = mvs
        new_his = now_state
        #
        shuffle_moves = np.copy(self.all_legal_moves)
        np.random.shuffle(shuffle_moves)
        print("new list seq: ")
        print(shuffle_moves)
        #
        for rm in shuffle_moves:
            print("\n")
            print("the move in right was: ", rm)
            if test_depth > 0:
                #
                valid_mov, new_his = self.next_move(rm, sheep_left, sheep_right, wolves_left, wolves_right, True
                                                    , now_state)
                print("in right move")
                print("new history is")
                print(new_his)
                #
                if valid_mov:
                    test_depth -= 1
                    #
                    non_d_sheep_mov, non_d_wolf_mov = rm
                    sheep_left -= non_d_sheep_mov
                    sheep_right += non_d_sheep_mov
                    wolves_left -= non_d_wolf_mov
                    wolves_right += non_d_wolf_mov
                    #
                    test_list.append(tuple(rm))
                    #
                    right_term = self.terminal(False, new_his)
                    if right_term:
                        #return test_list, rm
                        self.direction = False
                        self.states_history = new_his
                        self.sheep_left = sheep_left
                        self.sheep_right = sheep_right
                        self.wolves_left = wolves_left
                        self.wolves_right = wolves_right
                        return test_list
                    else:
                        #test_list, left_move = self.go_left(sheep_left, sheep_right, wolves_left, wolves_right
                        #                                    , new_his, mvs, depth_check)
                        test_list = self.go_left(sheep_left, sheep_right, wolves_left, wolves_right, new_his, mvs
                                                 , depth_check)
                    #left_score, left_move = self.go_left(self, sheep_left, sheep_right, wolves_left, wolves_right
                    #                                     , new_his, right_term, test_depth, a, b)
                    #left_score, left_move = self.go_left(self, sheep_left, sheep_right, wolves_left, wolves_right
                    #                                     , new_his, term, test_depth)
                    #
                #else:
                #    print("invalid move in right")
        self.direction = False
        self.states_history = new_his
        self.sheep_left = sheep_left
        self.sheep_right = sheep_right
        self.wolves_left = wolves_left
        self.wolves_right = wolves_right
        return test_list

    def go_left(self, sheep_left, sheep_right, wolves_left, wolves_right, now_state, mvs, depth_check):
        #
        term = self.terminal(False, now_state)
        if term or depth_check <= 0:
            return tuple()
        #
        #default_b = float("inf")
        #default_tuple = np.random.choice(np.array(self.all_legal_moves))
        test_depth = depth_check
        test_list = mvs
        new_his = now_state
        #
        shuffle_moves = np.copy(self.all_legal_moves)
        np.random.shuffle(shuffle_moves)
        #
        for lm in shuffle_moves:
            print("the move in left was: ", lm)
            if test_depth > 0:
                #
                valid_mov, new_his = self.next_move(lm, sheep_left, sheep_right, wolves_left, wolves_right, False
                                                    , now_state)
                print("in left move")
                print("new history is")
                print(new_his)
                #
                if valid_mov:
                    test_depth -= 1
                    #
                    non_d_sheep_mov, non_d_wolf_mov = lm
                    sheep_left -= non_d_sheep_mov
                    sheep_right += non_d_sheep_mov
                    wolves_left -= non_d_wolf_mov
                    wolves_right += non_d_wolf_mov
                    #
                    test_list.append(tuple(lm))
                    #
                    left_term = self.terminal(True, new_his)
                    if left_term:
                        #return test_list, lm
                        self.direction = True
                        self.states_history = new_his
                        self.sheep_left = sheep_left
                        self.sheep_right = sheep_right
                        self.wolves_left = wolves_left
                        self.wolves_right = wolves_right
                        return test_list
                    else:
                        #test_list, left_move = self.go_right(sheep_left, sheep_right, wolves_left, wolves_right
                        #                                    , new_his, mvs, depth_check)
                        test_list = self.go_right(sheep_left, sheep_right, wolves_left, wolves_right, new_his, mvs
                                                 , depth_check)
                    #left_score, left_move = self.go_right(self, sheep_left, sheep_right, wolves_left, wolves_right
                    #                                     , new_his, right_term, test_depth, a, b)
                    #left_score, left_move = self.go_right(self, sheep_left, sheep_right, wolves_left, wolves_right
                    #                                     , new_his, term, test_depth)
                    #
                #else:
                #    print("invalid move in left")
        self.direction = True
        self.states_history = new_his
        self.sheep_left = sheep_left
        self.sheep_right = sheep_right
        self.wolves_left = wolves_left
        self.wolves_right = wolves_right
        return test_list

    def search_a(self, depth):
        moves_list = []
        #while not self.terminal(self.direction, self.states_history):
            #
        if self.direction:
            #print("state_history")
            #print(self.states_history)
            ##print(self.states_history[-1:])
            #print(self.states_history[-1][:])
            #
            ans = self.go_right(self.sheep_left, self.sheep_right, self.wolves_left, self.wolves_right
                                , self.states_history, moves_list, depth)
        else:
            ans = self.go_left(self.sheep_left, self.sheep_right, self.wolves_left, self.wolves_right
                                , self.states_history, moves_list, depth)

        print("algo got the moves to be ", ans)
        #
        return ans

    def search_z(self, depth):
        # Add your code here! Your solve method should receive
        # the initial number of sheep and wolves as integers,
        # and return a list of 2-tuples that represent the moves
        # required to get all sheep and wolves from the left
        # side of the river to the right.
        #
        # If it is impossible to move the animals over according
        # to the rules of the problem, return an empty list of
        # moves.
        #
        moves_list_list = []
        #
        next_tuple = np.random.choice(np.array(self.all_legal_moves))
        #
        loop_depth = depth
        search_depth = depth
        #
        moves_list = []
        while not self.terminal(self.direction, self.states_history):
            #
            if self.direction:
                #
                next_tuple = self.go_right(self.sheep_left, self.sheep_right, self.wolves_left, self.wolves_right,
                                           self.states_history, self.direction, moves_list, depth)
            else:
                next_tuple = self.go_left(self.sheep_left, self.sheep_right, self.wolves_left, self.wolves_right,
                                           self.states_history, self.direction, moves_list, depth)

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
        self.states_history = np.vstack((self.states_history, new_state))
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
        #print("history")
        #print(self.states_history)
        #print(self.states_history.shape)
        #print(self.states_history[-1:])
        depth = 0
        if initial_sheep >= 10:
            depth = initial_wolves + initial_sheep + 5
        else:
            depth = 10 * initial_sheep
        #
        while self.sheep_left + self.wolves_left > 0:
            # next_move = self.search(depth)
            # moves_list.append(next_move)
            moves_list = self.search_a(depth)
            print("real_solve")
            print("moves_list solution\n", moves_list)
            print("stop here")
        return moves_list
