import numpy as np
from numpy import sort


# import heapq


class SemanticNetsAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_sam, initial_onering, initial_frodo, initial_gollum):
        agents_agent = OneRingAndRiver()
        return agents_agent.search_bfs(initial_sam, initial_onering, initial_frodo, initial_gollum)


class OneRingAndRiver:
    def __init__(self):
        # binary direction value True means next move is right
        self.direction = True
        self.total_players = 0
        self.all_legal_moves = [(1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (1, 0, 0, 0)]
        # Sam-L, #Sam-R,
        # OR-L, OR-R
        # F-L, F-R
        # G-L, G-R
        # Direction
        self.states_history = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])
        # the teams
        self.sam_left = 0
        self.sam_right = 0
        self.onering_left = 0
        self.onering_right = 0
        self.frodo_left = 0
        self.frodo_right = 0
        self.gollum_left = 0
        self.gollum_right = 0

    def check_move(self, sam_left, sam_right, onering_left, onering_right, frodo_left, frodo_right, gollum_left
                   , gollum_right, direction):
        if sam_left < 0 or sam_right < 0 or onering_left < 0 or onering_right < 0 or frodo_left < 0 or frodo_right < 0 \
                or gollum_left < 0 or gollum_right < 0:
            print("failed bc - (sam_left < 0 or sam_right < 0 or onering_left < 0 or onering_right < 0)")
            return False
        elif (onering_left > sam_left) and ((gollum_left > 0) or (frodo_left > 0)):
            print("failed bc - (onering_left > sam_left) and ((gollum_left > 0) or (frodo_left > 0)")
            return False
        elif (onering_right > sam_right) and ((gollum_right > 0) or (frodo_right > 0)):
            print("failed bc - (onering_right > sam_right) and ((gollum_right > 0) or (frodo_right > 0)")
            return False
        elif sam_left + onering_left + frodo_left + gollum_left == self.total_players:
            print("failed bc - (sam_left + onering_left + frodo_left + gollum_left == self.total_players)")
            return False
        # elif (sam_left == 0 and onering_right == 0) and direction is False:
        #     return False
        # elif (onering_right + sam_right == 1) and direction is False:
        #     #elif (onering_right + sam_right == 1) and self.total_players < 5 and direction is False:
        #     # print("failed bc - ((onering_right + sam_right == 1) and direction is False)")
        #     # elif (onering_right == 1) and direction is False:
        #     return False
        else:
            return True

    def state_check(self, sam_left, sam_right, onering_left, onering_right, frodo_left, frodo_right, gollum_left
                    , gollum_right, direction, st_hist):
        new_move = np.array([[sam_left, sam_right, onering_left, onering_right, frodo_left, frodo_right, gollum_left
                                 , gollum_right, direction]])
        states_copy = np.copy(st_hist)
        new_states = np.vstack((states_copy, new_move))
        unique_moves = np.unique(new_states, axis=0)
        #
        # if np.equal(new_states, unique_moves).all():
        if new_states.shape == unique_moves.shape:
            return True, new_states
        else:
            return False, states_copy

    def next_move(self, mov, sam_left, sam_right, onering_left, onering_right, frodo_left, frodo_right, gollum_left
                  , gollum_right, direction, history):
        #
        non_d_sam_mov, non_d_onering_mov, non_d_frodo_mov, non_d_gollum_mov = mov
        if direction:
            sam_left -= non_d_sam_mov
            sam_right += non_d_sam_mov
            onering_left -= non_d_onering_mov
            onering_right += non_d_onering_mov
            #
            frodo_left -= non_d_frodo_mov
            frodo_right += non_d_frodo_mov
            gollum_left -= non_d_gollum_mov
            gollum_right += non_d_gollum_mov
        else:
            sam_left += non_d_sam_mov
            sam_right -= non_d_sam_mov
            onering_left += non_d_onering_mov
            onering_right -= non_d_onering_mov
            #
            frodo_left += non_d_frodo_mov
            frodo_right -= non_d_frodo_mov
            gollum_left += non_d_gollum_mov
            gollum_right -= non_d_gollum_mov
        #########
        # check #
        #########
        # print("check the check_move")
        mov_check_ = self.check_move(sam_left, sam_right, onering_left, onering_right, frodo_left, frodo_right
                                     , gollum_left, gollum_right, not direction)
        if mov_check_:
            st_check_, st_hist = self.state_check(sam_left, sam_right, onering_left, onering_right
                                                  , frodo_left, frodo_right, gollum_left, gollum_right
                                                  , not direction, history)
            if st_check_:
                return True, st_hist
        return False, history

    def bfs(self):
        # default_tuple = np.random.choice(np.array(self.all_legal_moves))
        #
        shuffle_moves = np.copy(self.all_legal_moves)
        np.random.shuffle(shuffle_moves)
        default_tuple = tuple(shuffle_moves[0])
        default_score = float("-inf")
        # default_tuple = self.all_legal_moves[0]
        #
        new_his = self.states_history
        valid_count = 0
        #
        for mv in shuffle_moves:
            print("legal move was: ")
            print(mv)
            print("with direction: ")
            print(self.direction)
            valid_mov, temp_new_his = self.next_move(mv, self.sam_left, self.sam_right
                                                , self.onering_left, self.onering_right
                                                , self.frodo_left, self.frodo_right
                                                , self.gollum_left, self.gollum_right
                                                , self.direction, self.states_history)
            #
            if valid_mov:
                print("state was legal")
                print("what was the history")
                print(self.states_history)
                print("what is new history")
                print(temp_new_his)
                # #
                # print(new_his)
                valid_count += 1
                ####
                non_d_sam_mov, non_d_onering_mov, non_d_frodo_mov, non_d_gollum_mov = mv
                ##
                # check score
                if self.direction:
                    if (self.sam_right + non_d_sam_mov + self.onering_right + non_d_onering_mov + self.frodo_right +
                            non_d_frodo_mov + self.gollum_right + non_d_gollum_mov) > default_score:
                        default_score = self.sam_right + non_d_sam_mov + self.onering_right + non_d_onering_mov + \
                                        self.frodo_right + non_d_frodo_mov + self.gollum_right + non_d_gollum_mov
                        default_tuple = tuple(mv)
                        new_his = temp_new_his
                else:
                    if (self.sam_right - non_d_sam_mov + self.onering_right - non_d_onering_mov + self.frodo_right -
                            non_d_frodo_mov + self.gollum_right - non_d_gollum_mov) > default_score:
                        default_score = self.sam_right - non_d_sam_mov + self.onering_right - non_d_onering_mov + \
                                        self.frodo_right - non_d_frodo_mov + self.gollum_right - non_d_gollum_mov
                        default_tuple = tuple(mv)
                        new_his = temp_new_his
            #
            else:
                print("state was illegal")
                print("breakpoint")
        if valid_count > 0:
            non_d_sam_mov, non_d_onering_mov, non_d_frodo_mov, non_d_gollum_mov = default_tuple
            if self.direction:
                self.sam_left -= non_d_sam_mov
                self.sam_right += non_d_sam_mov
                self.onering_left -= non_d_onering_mov
                self.onering_right += non_d_onering_mov
                #
                self.frodo_left -= non_d_frodo_mov
                self.frodo_right += non_d_frodo_mov
                self.gollum_left -= non_d_gollum_mov
                self.gollum_right += non_d_gollum_mov
            else:
                self.sam_left += non_d_sam_mov
                self.sam_right -= non_d_sam_mov
                self.onering_left += non_d_onering_mov
                self.onering_right -= non_d_onering_mov
                #
                self.frodo_left += non_d_frodo_mov
                self.frodo_right -= non_d_frodo_mov
                self.gollum_left += non_d_gollum_mov
                self.gollum_right -= non_d_gollum_mov

            print("what is the history")
            print(new_his)
            self.states_history = new_his
            self.direction = not self.direction
            ####
            return default_tuple, valid_count
            # return mv, valid_count
        # if valid_count == 0:
        #     print("no valid move")
        #
        return default_tuple, valid_count

    def search_bfs(self, sam_left, onering_left, frodo_left, gollum_left):
        moves_list = []
        #
        self.total_players = sam_left + onering_left + frodo_left + gollum_left
        self.sam_left = sam_left
        self.onering_left = onering_left
        #
        self.frodo_left = frodo_left
        self.gollum_left = gollum_left
        #
        self.states_history[0, 0] = self.sam_left
        self.states_history[0, 1] = self.sam_right
        self.states_history[0, 2] = self.onering_left
        self.states_history[0, 3] = self.onering_right
        #
        self.states_history[0, 4] = self.frodo_left
        self.states_history[0, 5] = self.frodo_right
        self.states_history[0, 6] = self.gollum_left
        self.states_history[0, 7] = self.gollum_right
        #
        self.states_history[0, 8] = self.direction
        #
        global_reset = 0
        # catch_reset = 0
        while self.sam_left + self.onering_left + self.frodo_left + self.gollum_left > 0:
            mov, validate = self.bfs()
            # if validate == 0 and global_reset < 900:
            if validate == 0:
                self.__init__()
                # print("here?")
                self.total_players = sam_left + onering_left + frodo_left + gollum_left
                self.sam_left = sam_left
                self.onering_left = onering_left
                #
                self.frodo_left = frodo_left
                self.gollum_left = gollum_left
                #
                self.states_history[0, 0] = self.sam_left
                self.states_history[0, 1] = self.sam_right
                self.states_history[0, 2] = self.onering_left
                self.states_history[0, 3] = self.onering_right
                #
                self.states_history[0, 4] = self.frodo_left
                self.states_history[0, 5] = self.frodo_right
                self.states_history[0, 6] = self.gollum_left
                self.states_history[0, 7] = self.gollum_right
                #
                self.states_history[0, 8] = self.direction
                global_reset += 1
                if global_reset < 899:
                    moves_list = []
            elif global_reset >= 900:
                 return moves_list
            else:
                moves_list.append(mov)
        return moves_list


class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        nums.sort()
        return_list = []
        # return_list.append(1, 2)
        for i in range(2, len(nums) - 1):
            diff_sum = target - nums[i]
            if diff_sum == nums[i + 1]:
                return_list.append(i)
                return_list.append(i+1)
                return return_list
        return False

