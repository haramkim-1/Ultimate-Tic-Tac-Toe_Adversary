from random import randint
import copy

class Node:
    moves = {}
    wins = 1
    trials = 1

class MonteCarloBot:
    
    def get_move(self, pos, tleft):
        lmoves = pos.legal_moves()
        rm = randint(0, len(lmoves)-1)
        return lmoves[rm]

    def monte_carlo(self, pos, iterations, explore_parameter):
        cur_pos = copy.deepcopy(pos)


