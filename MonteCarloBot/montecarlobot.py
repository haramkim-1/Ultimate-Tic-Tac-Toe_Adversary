import random
from random import randint
import copy
from enum import Enum
import bisect
import sys

class Node:
    moves = {}
    wins = {}
    trials = -1

    def __init__(self, trials):
        self.trials = trials
        moves = {}

class Victory(Enum):
    WIN = 1
    LOSE = -1
    DRAW = 0

class MonteCarloBot:

    myid = -1
    oppid = -1

    def __init__(self):
        self.log = open("montecarlo_log.log", "a+")
        self.log.write("\n\n")
        self.log.flush

    def other_player(self, pid):
        if pid == self.myid:
            return self.oppid
        else:
            return self.myid

    def monte_carlo_iter(self, pos, node, turn):
        self.log.write("\t"+str(pos.legal_moves())+": ")
        self.log.flush()
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
        self.log.write("\t BEFORE MAKE CHILDREN: " + str(node.moves.keys())+": ")
        self.log.flush()
        if not node.moves:
            self.log.write("\t MAKING CHILDREN : ")
            self.log.flush()
            for i in moves:
                node.moves[i] = Node(2)
                node.moves[i].wins[self.myid] = 1
                node.moves[i].wins[self.oppid] = 1
                node.moves[i].moves = {}
        weights = [0]*l
        total = 0
        for i in range(0,l):
            assert node.moves
            #try:
            m = node.moves[moves[i]]
            #except Exception as e:
            #    raise Exception(str(node.moves.keys()) + "\n\n\n" + str(moves))
            weights[i] = m.wins[turn]/m.trials
            total = total + weights[i]
        weights = [i/total for i in weights]
        for i in range(1,l):
            weights[i] = weights[i] + weights[i-1]
        num = random.random()
        choice = bisect.bisect(weights, num)
        self.log.write(str(moves[choice])+"\n")
        self.log.flush()
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
        self.log.write(str(pos.legal_moves())+"\n")
        self.log.flush()
        root = Node(2)
        root.wins[self.myid] = 1
        root.wins[self.oppid] = 1
        root.moves = {}
        #print("\n\n\niterating\n\n\n")
        for i in range(0,iterations):
            #if i > 0:
            #    raise Exception("abc")
            #print("\n\n\nrunning iteration: "+ str(i) + "\n\n\n")
            self.monte_carlo_iter(copy.deepcopy(pos), root, self.myid)
            self.log.write("\nFINISH ITER\n")
            self.log.flush()
        
        #var = max(root.moves.items(), key=lambda item: item[1].wins[self.myid]/item[1].trials)[0]
        #print("\n\n\n\ntype: " + str(type(var)) + "\n\n\n\n")
        move = max(root.moves.items(), key=lambda item: item[1].wins[self.myid]/item[1].trials)[0]
        self.log.write(str(move)+"\n")
        self.log.flush()
        return move

    def get_move(self, pos, tleft):
        #return self.monte_carlo(pos, 1000)
        #print("GET MOVE RUNNING")
        num_moves = len(pos.legal_moves())
        return self.monte_carlo(pos, 100*num_moves+300)

        #lmoves = pos.legal_moves()
        #rm = randint(0, len(lmoves)-1)
        #return lmoves[rm]
