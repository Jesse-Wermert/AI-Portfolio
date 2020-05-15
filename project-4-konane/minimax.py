from updatedKonane import Konane, Player, KonaneError, RandomPlayer
from alarm import *

class MinimaxNode:
    """
    Black always goes first and is considered the maximizer.
    White always goes second and is considered the minimizer.
    """
    def __init__(self, state, last_move, depth, player):
        self.state = state  # current board configuration
        self.operator = last_move  # the move that resulted in the current board configuration
        self.depth = depth  # the depth of the node in the search tree
        self.player = player  # maximizer or minimizer

    def get_maximizer(self):
        """
        Gets the maximizer (the black piece "B")
        """
        return "B"

    def get_minimizer(self):
        """
        Gets the minimizer (the white piece "W").
        """
        return "W"

    def is_root(self):
        """
        :return: True if node is root node, False otherwise.
        """
        return self.depth == 0

    def is_maximizer(self):
        """
        :return: True if node is maximizing node ('B'), False otherwise.
        """
        return self.player == 'B'

    def is_minimizer(self):
        """
        :return: True  if node minimizing node ('W'), False otherwise.
        """
        return self.player == 'W'

    def __str__(self):
        result = "\nState: " + str(self.state)
        result += "\nDepth: " + str(self.depth)
        result += "\nPlayer: " + str(self.player)
        result += "\nOperator: " + str(self.operator)
        return result


class MinimaxPlayer(Konane, Player):

    def __init__(self, size, depthLimit):
        Konane.__init__(self, size)
        Player.__init__(self)
        self.limit = depthLimit
        self.bestMove = None
        self.INFINITY = 5000

    def initialize(self, side):
        """
        Initializes the player's color and name.
        """
        self.side = side
        self.name = "MinimaxDepth " + str(self.limit) + " Wermert"

    @timed_out(3)
    def getMove(self, board):
        """
        Returns the chosen move based on doing an alphaBetaMinimax
        search.
        """
        root = MinimaxNode(board, None, 0, self.side)
        self.alphaBetaMinimax(root, -self.INFINITY, self.INFINITY)
        return self.bestMove

    def staticEval(self, node):
        """
        Returns an estimate of the value of the state associated
        with the given node. Another way to say that is: the static
        evaluator funtion will return the static value of the
        current game state.
        """
        num_max_moves = self.max_moves(node)
        num_min_moves = self.min_moves(node)
        if node.get_minimizer() == node.player and num_min_moves == 0:
            return self.INFINITY
        if node.get_maximizer() == node.player and num_max_moves == 0:
            return -self.INFINITY
        value = num_max_moves - num_min_moves
        return value

    def successors(self, node):
        """
        Returns a list of the successor nodes for the given node.
        """
        successor_nodes = []
        for move in self.generateMoves(node.state, node.player):
            next_board_state = self.nextBoard(node.state, node.player, move)
            next_node = MinimaxNode(next_board_state, move, node.depth + 1, self.opponent(node.player))
            successor_nodes.append(next_node)
        return successor_nodes

    def alphaBetaMinimax(self, node, alpha, beta):
        """
        Returns the best score for the player associated with the
        given node.  Also sets the instance variable bestMove to the
        move associated with the best score at the root node.
        Initialize alpha to -infinity and beta to +infinity.
        """
        if node.depth == self.limit:
            return self.staticEval(node)
        successors = self.successors(node)
        if len(successors) == 0:
            if node.is_root():
                self.bestMove = []
            return self.staticEval(node)
        if node.is_root():
            self.bestMove = successors[0].operator
            if len(successors) == 1:
                return None
        if node.is_maximizer():
            return self.maxV(successors, node, alpha, beta)
        else:
            return self.minV(successors, node, alpha, beta)

    def minV(self, successors, node, alpha, beta):
        """
        Minimax Alpha-Beta Pruning minimizer fcn., which calculates the
        value for beta
        :return: the calculated value for beta
        """
        for i in range(len(successors)):
            v = self.alphaBetaMinimax(successors[i], alpha, beta)
            if v < beta:
                beta = v
                if node.depth == 0:
                    self.bestMove = successors[i].operator
            if beta <= alpha:
                return beta
        return beta

    def maxV(self, successors, node, alpha, beta):
        """
        Minimax Alpha-Beta Pruning maximizer fcn., which calculates the
        value for alpha
        :return: the calculated value for alpha
        """
        for i in range(len(successors)):
            v = self.alphaBetaMinimax(successors[i], alpha, beta)
            if v > alpha:
                alpha = v
                if node.depth == 0:
                    self.bestMove = successors[i].operator
            if alpha >= beta:
                return alpha
        return alpha

    def max_moves(self, node):
        """
        :param node: The given maximizer node
        :return: the number of maximizer moves
        """
        return len(self.generateMoves(node.state, node.get_maximizer()))

    def min_moves(self, node):
        """
        :param node: The given minimizer node
        :return: the number of minimizer nodes
        """
        return len(self.generateMoves(node.state, node.get_minimizer()))


# game = Konane(8)
# game.playNGames(20, MinimaxPlayer(8, 3), RandomPlayer(8))
