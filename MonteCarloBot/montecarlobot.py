import random
import copy
from enum import Enum
import bisect

class Node:
    moves = {}
    wins = {}
    trials = -1

    def __init__(self, trials):
        self.trials = trials

class Victory(Enum):
    WIN = 1
    LOSE = -1
    DRAW = 0

class MonteCarloBot:

    myid = -1
    oppid = -1

    def other_player(self, pid):
        if pid == self.myid:
            return self.oppid
        else:
            return self.myid

    def monte_carlo_iter(self, pos, node, turn):
        vic = pos.check_victory()
        if vic == self.myid:
            return Victory.WIN
        elif vic == self.oppid:
            return Victory.LOSE
        moves = pos.legal_moves()
        if not moves:
            return Victory.DRAW
        l = len(moves)
        if not node.moves:
            for i in moves:
                node.moves[i] = Node(2)
                node.wins[self.myid] = 1
                node.wins[self.oppid] = 1
        weights = []*l
        total = 0
        for i in range(0,l):
            weights[i] = node.moves[i].wins[turn]/node.moves[i].trials
            total = total + weights[i]
        weights = [i/total for i in weights]
        for i in range(1,l):
            weights[i] = weights[i] + weights[i-1]
        num = random.random()
        choice = bisect.bisect(weights, num)
        result = self.monte_carlo_iter(pos.make_move(moves[choice], turn), node.moves[moves[choice]], turn.other())
        node.trials = node.trials + 1
        if result == Victory.WIN:
            node.wins[self.oppid] = node.wins[self.oppid] + 1
            return Victory.LOSE
        elif result == Victory.LOSE:
            node.wins[self.myid] = node.wins[self.myid] + 1
            return Victory.LOSE
        else:
            return Victory.DRAW

    def monte_carlo(self, pos, iterations):
        root = Node(2)
        for i in range(0,iterations):
            self.monte_carlo_iter(copy.deepcopy(pos), root, self.myid)
        max = 0
        for (move, node) in (root.moves).items():
            if node.wins/node.trials > max:
                max = node.wins/node.trials
                argmax = move
        return argmax

    def get_move(self, pos, tleft):
        return self.monte_carlo(pos, 10000)