from informedSearch import InformedProblemState, InformedNode, InformedSearch
GOAL = [1, 2, 3, 8, 0, 4, 7, 6, 5]


class EightPuzzle(InformedProblemState):
    """
    The eight puzzle consists of a three by three board with eight
    numbered tiles and a blank space. A tile adjacent to the blank
    space can slide into the space. The object is to figure out the
    steps needed to get from one configuration of the tiles to
    another.

    For this problem, a state should specify the location of each
    of the eight tiles as well as the blank space in the three by
    three grid. The operators are most efficiently represented
    as moving the blank left, right, up, or down, rather than
    creating operators for each of the numbered tiles.
    """
    def __init__(self, board, operator=None):
        self.board = board
        self.operator = operator

    def goal_test(self):
        return self.board == GOAL

    def get_blank_piece(self):
        return self.board.index(0)

    def shift_right(self):
        """
        Shift the blank piece right.
        """
        copy = self.board[:]
        blank = self.get_blank_piece()
        if blank not in [2, 5, 8]:
            to_move = blank + 1
            copy[blank], copy[to_move] = copy[to_move], copy[blank]
            return EightPuzzle(copy, "RIGHT")
        # return None

    def shift_left(self):
        """
        Shift the blank piece left.
        """
        copy = self.board[:]
        blank = self.get_blank_piece()
        if blank not in [0, 3, 6]:
            to_move = blank - 1
            copy[blank], copy[to_move] = copy[to_move], copy[blank]
            return EightPuzzle(copy, "LEFT")
        # return None

    def shift_up(self):
        """
        Shift the blank space up.
        """
        copy = self.board[:]
        blank = self.get_blank_piece()
        if blank not in [0, 1, 2]:
            to_move = blank - 3
            copy[blank], copy[to_move] = copy[to_move], copy[blank]
            return EightPuzzle(copy, "UP")
        # return None

    def shift_down(self):
        """
        Shift the blank space down.
        """
        copy = self.board[:]
        blank = self.get_blank_piece()
        if blank not in [6, 7, 8]:
            copy[blank], copy[blank+3] = copy[blank+3], copy[blank]
            return EightPuzzle(copy, "DOWN")
        # return None

    def __str__(self):
        result = ""
        if self.operator is None:
            result += "Initial State" + "\n"
        elif self.operator is not None:
            result += str(self.operator) + "\n"
        for i in self.board:
            if i != 0:
                result += str(i)
            elif i == 0:
                result += "_"
            if self.board.index(i) in (2, 5, 8):
                result += "\n"
        return result

    def dictkey(self):
        result = ""
        for i in self.board:
            result += str(i) + ","
        return result

    def applyOperators(self):
        operators = []
        if self.shift_left() is not None:
            operators.append(self.shift_left())
        if self.shift_right() is not None:
            operators.append(self.shift_right())
        if self.shift_up() is not None:
            operators.append(self.shift_up())
        if self.shift_down() is not None:
            operators.append(self.shift_down())
        return operators

    def equals(self, state):
        return self.board == state.board

    def heuristic(self, goal_state):
        # summation = self.t_o_o_p(goal_state)
        summation = self.manhattan(goal_state)
        return summation

    def manhattan(self, goal_state):
        """
        Manhattan distance heuristic function.
        :param goal_state:
        :return:
        """
        dist = 0
        for tile in range(len(self.board)):
            if self.board[tile] == 0:
                pass
            elif self.board[tile] != 0:  # case of blank tile => *Ignore*
                dx, dy = self.board.index(tile) % 3, self.board.index(tile) // 3
                # g_dx, g_dy = GOAL.index(tile) % 3, GOAL.index(tile) // 3
                g_dx, g_dy = goal_state.board.index(tile) % 3, goal_state.board.index(tile) // 3
                dist += abs(dx - g_dx) + abs(dy - g_dy)
        return dist

    def t_o_o_p(self, goal_state):
        """
        Tiles out of place heuristic function.
        :param goal_state:
        :return:
        """
        dist = 0
        for tile in range(len(self.board)):
            if self.board[tile] == 0:
                pass
            elif self.board[tile] != goal_state.board[tile]:
                dist += 1
        return dist


a = EightPuzzle([0, 1, 3, 8, 2, 4, 7, 6, 5])
b = EightPuzzle([1, 3, 4, 8, 6, 2, 0, 7, 5])
c = EightPuzzle([1, 3, 0, 4, 2, 5, 8, 7, 6])
d = EightPuzzle([7, 1, 2, 8, 0, 3, 6, 5, 4])
e = EightPuzzle([8, 1, 2, 7, 0, 4, 6, 5, 3])
f = EightPuzzle([2, 6, 3, 4, 0, 5, 1, 8, 7])
g = EightPuzzle([7, 3, 4, 6, 1, 5, 8, 0, 2])
h = EightPuzzle([7, 4, 5, 6, 0, 3, 8, 1, 2])
goal = EightPuzzle([1, 2, 3, 8, 0, 4, 7, 6, 5])
i = EightPuzzle([0, 1, 2, 3, 4, 5, 6, 7, 8])  # Challenge puzzle a
j = EightPuzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])  # Challenge puzzle b
# a_search = InformedSearch(a, goal)
# a_search = InformedSearch(a, goal, True)
# print(a_search.get_expansions())  # dist: 3, tiles: 3
# b_search = InformedSearch(b, goal)
# b_search = InformedSearch(b, goal, True)
# print(b_search.get_expansions())  # dist: 7, tiles: 8
# c_search = InformedSearch(c, goal)
# c_search = InformedSearch(c, goal, True)
# print(c_search.get_expansions())  # dist: 15, tiles: 17
# d_search = InformedSearch(d, goal)
# d_search = InformedSearch(d, goal, True)
# print(d_search.get_expansions())
# e_search = InformedSearch(e, goal)
# e_search = InformedSearch(e, goal, True)
# print(e_search.get_expansions())
# f_search = InformedSearch(f, goal)
# f_search = InformedSearch(f, goal, True)
# print(f_search.get_expansions())
# g_search = InformedSearch(g, goal)
# g_search = InformedSearch(g, goal, True)
# print(g_search.get_expansions())
# h_search = InformedSearch(h, goal)
# h_search = InformedSearch(h, goal, True)
# print(h_search.get_expansions())
# i_search = InformedSearch(i, goal, True)  # not solvable here
# j_search = InformedSearch(j, goal, True)  # not solvable here



# note if it says a number a/b, a is old value,  b is new value

# Node Expansions
#################################
# Problem  A*(tiles)   A*(dist) #
#  A          3          3      #
#  B          8          7      #
#  C          14         15     #
#  D          39         22     #
#  E          39         38     #
#  F          87         23     #
#  G          332        70     #
#  H          3780       357    #
#################################
