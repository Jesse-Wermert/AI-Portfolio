from search import ProblemState, Search
from improvedSearch import ImprovedSearch
LEGAL_STATES = [[2, 3, 0], [0, 3, 0], [2, 3, 1], [1, 3, 1], [1, 1, 0],
                [2, 2, 1], [0, 2, 0], [0, 3, 1], [0, 1, 0], [0, 2, 1],
                [1, 1, 1], [0, 0, 0], [3, 3, 1], [1, 3, 0], [2, 2, 0]]


class MissionaryState(ProblemState):

    def __init__(self, missionaries, cannibals, boat, operator=None):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat = boat
        self.operator = operator
        self.value = [missionaries, cannibals, boat]

    def __str__(self):
        result = ""
        if self.operator is not None:
            result += "Operator: " + self.operator + "\n"
        result += str(self.missionaries) + "," + str(self.cannibals) + "," + str(self.boat)
        return result

    def boat_on_right(self):
        return self.boat == 0

    def boat_on_left(self):
        return self.boat == 1

    def return_1m(self):
        return MissionaryState(self.missionaries + 1, self.cannibals, self.boat + 1, "1m at boat dock")

    def return_1c(self):
        return MissionaryState(self.missionaries, self.cannibals + 1, self.boat + 1, "1c at boat dock")

    def send_1m(self):
        return MissionaryState(self.missionaries - 1, self.cannibals, self.boat - 1, "send1m over")

    def send_2m(self):
        return MissionaryState(self.missionaries - 2, self.cannibals, self.boat - 1, "send2m over")

    def send_1c(self):
        return MissionaryState(self.missionaries, self.cannibals - 1, self.boat - 1, "send1c over")

    def send_2c(self):
        return MissionaryState(self.missionaries, self.cannibals - 2, self.boat - 1, "send2c over")

    def send_1m_1c(self):
        return MissionaryState(self.missionaries - 1, self.cannibals - 1, self.boat - 1, "send1m1c over")

    def return_1m_1c(self):
        return MissionaryState(self.missionaries + 1, self.cannibals + 1, self.boat + 1, "1m1c at boat dock")

    def equals(self, state):
        return self.value == state.value

    def dict_key(self):
        return str(self.missionaries) + "," + str(self.cannibals) + "," + str(self.boat)

    def applyOperators(self):
        valid_successors = []
        if self.send_1m().value in LEGAL_STATES:
            valid_successors.append(self.send_1m())
        if self.send_2m().value in LEGAL_STATES:
            valid_successors.append(self.send_2m())
        if self.send_1c().value in LEGAL_STATES:
            valid_successors.append(self.send_1c())
        if self.send_2c().value in LEGAL_STATES:
            valid_successors.append(self.send_2c())
        if self.send_1m_1c().value in LEGAL_STATES:
            valid_successors.append(self.send_1m_1c())
        if self.return_1c().value in LEGAL_STATES:
            valid_successors.append(self.return_1c())
        if self.return_1m().value in LEGAL_STATES:
            valid_successors.append(self.return_1m())
        if self.return_1m_1c().value in LEGAL_STATES:
            valid_successors.append(self.return_1m_1c())
        return valid_successors


Search(MissionaryState(3, 3, 1), MissionaryState(0, 0, 0), True)
print("----------------------------------------------------------------------------------------------------------------")
ImprovedSearch(MissionaryState(3, 3, 1), MissionaryState(0, 0, 0), True)
