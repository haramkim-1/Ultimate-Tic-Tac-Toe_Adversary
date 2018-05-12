import random
from random import randint
import copy
from enum import Enum
import bisect
import tkinter
from tkinter import messagebox

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
        vic = pos.checkMacroboardWinner()
        #print(pos)
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
                node.moves[i].wins[self.myid] = 1
                node.moves[i].wins[self.oppid] = 1
        weights = [0]*l
        total = 0
        for i in range(0,l):
            m = node.moves[moves[i]]
            weights[i] = m.wins[turn]/m.trials
            total = total + weights[i]
        weights = [i/total for i in weights]
        for i in range(1,l):
            weights[i] = weights[i] + weights[i-1]
        num = random.random()
        choice = bisect.bisect(weights, num)
        pos.make_move(moves[choice], turn)
        result = self.monte_carlo_iter(pos, node.moves[moves[choice]], self.other_player(turn))
        node.trials = node.trials + 1
        if result == Victory.WIN:
            node.wins[self.oppid] = node.wins[self.oppid] + 1
            return Victory.LOSE
        elif result == Victory.LOSE:
            node.wins[self.myid] = node.wins[self.myid] + 1
            return Victory.WIN
        else:
            return Victory.DRAW

    def monte_carlo(self, pos, iterations):
        root = Node(2)
        root.wins[self.myid] = 1
        root.wins[self.oppid] = 1
        #print("\n\n\niterating\n\n\n")
        for i in range(0,iterations):
            #print("\n\n\nrunning iteration: "+ str(i) + "\n\n\n")
            self.monte_carlo_iter(copy.deepcopy(pos), root, self.myid)
        
        #var = max(root.moves.items(), key=lambda item: item[1].wins[self.myid]/item[1].trials)[0]
        #print("\n\n\n\ntype: " + str(type(var)) + "\n\n\n\n")
        return max(root.moves.items(), key=lambda item: item[1].wins[self.myid]/item[1].trials)[0]

    def get_move(self, pos, tleft):
        #return self.monte_carlo(pos, 1000)
        #print("GET MOVE RUNNING")
        return self.monte_carlo(pos, 500)

        #lmoves = pos.legal_moves()
        #rm = randint(0, len(lmoves)-1)
        #return lmoves[rm]
