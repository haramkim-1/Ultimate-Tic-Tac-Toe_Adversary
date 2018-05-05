import random
import copy
from enum import Enum
import bisect

class Node:
    moves = {}
    wins = []
    trials = -1

    def __init__(self, wins, trials):
        self.wins = wins
        self.trials = trials

class Victory(Enum):
    WIN = 1
    LOSE = -1
    DRAW = 0

class Turn(Enum):
    MINE = 0
    ENEMY = 1

    def other(self):
        if self == Turn.ENEMY:
            return Turn.MINE
        else:
            return Turn.ENEMY

class MonteCarloBot:

    myid = -1
    oppid = -1
    
    def get_move(self, pos, tleft):
        lmoves = pos.legal_moves()
        rm = 0#randint(0, len(lmoves)-1)
        return lmoves[rm]

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
                node.moves[i] = Node([1,1], l)
        weights = []*l
        total = 0
        for i in range(0,l):
            weights[i] = node.moves[i].wins[turn]
            total = total + node.trials 
        weights = [i/total for i in weights]
        for i in range(1,l):
            weights[i] = weights[i] + weights[i-1]
        num = random.random()
        choice = bisect.bisect(weights, num)
        result = self.monte_carlo_iter(pos.make_move(moves[choice]), node.moves[moves[choice]], turn.other())
        node.trials = node.trials + 1
        if result == Victory.WIN:
            node.wins[Turn.ENEMY] = node.wins[Turn.ENEMY] + 1
            return Victory.LOSE
        elif result == Victory.LOSE:
            node.wins[Turn.MINE] = node.wins[Turn.MINE] + 1
            return Victory.LOSE
        else:
            return Victory.DRAW

    def monte_carlo(self, pos, iterations):
        cur_pos = copy.deepcopy(pos)


