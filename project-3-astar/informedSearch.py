from pq import PriorityQueue
from search import Node, Search, ProblemState
from abc import ABC, abstractmethod


class InformedProblemState(ProblemState):
    """
    Implement this.
    """
    @abstractmethod
    def heuristic(self, goal_state):
        pass

    @abstractmethod
    def applyOperators(self):
        pass

    @abstractmethod
    def equals(self, state):
        pass

    @abstractmethod
    def dictkey(self):
        pass


class InformedNode(Node):
    """
    Implement this.
    """
    def __init__(self, state, parent, depth, goal_state):
        Node.__init__(self, state, parent, depth)
        self.goal_state = goal_state

    def __str__(self):
        result = "\nState: " + str(self.state)
        result += "\nDepth: " + str(self.depth)
        if self.parent != None:
            result += "\nParent: " + str(self.parent.state)
        return result

    def priority(self):
        """
        Needed to determine where the node should be placed in the
        priority queue.  Depends on the current depth of the node as
        well as the estimate of the distance from the current state to
        the goal state.
        """
        return self.depth + self.state.heuristic(self.goal_state)


class InformedSearch(Search):
    """
    Implement this.
    """

    def __init__(self, initial_state, goal_state, verbose=False):
        self.node_expansions = 0
        self.unique_states = {}
        self.unique_states[initial_state.dictkey()] = True
        self.q = PriorityQueue()
        self.goal_state = goal_state
        self.q.enqueue(InformedNode(initial_state, None, 0, self.goal_state))
        self.verbose = verbose
        solution = self.execute()
        if solution is None:
            print("Search failed")
        else:
            self.showPath(solution)

    def execute(self):
        while not self.q.empty():
            current = self.q.dequeue()
            self.node_expansions += 1
            if self.goal_state.equals(current.state):
                return current
            else:
                successors = current.state.applyOperators()
                for next_state in successors:
                    if next_state.dictkey() not in self.unique_states.keys():
                        n = InformedNode(next_state, current, current.depth + 1, self.goal_state)
                        self.q.enqueue(n)
                        self.unique_states[next_state.dictkey()] = True
                    if self.verbose:
                        print("Expanded:", current)
                        print("Number of successors:", len(successors))
                        print("Queue length: ", self.q.size())
                        print("-------------------------------")
        return None

    def get_expansions(self):
        return self.node_expansions
