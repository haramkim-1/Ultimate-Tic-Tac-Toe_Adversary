import copy
import sys


class MinimaxBot:

    myid = -1
    oppid = -1
    minval = -999999999
    maxval = -minval

    def __init__(self):
        self.log = open("minimax_log.log", "a+")
        self.log.write("\n\n")
        self.log.flush

    def get_move(self, pos, tleft):
        self.log.write(str(pos.legal_moves())+": ")
        self.log.flush()
        lmoves = pos.legal_moves()
        # TODO: initialize this to the first move in lmoves?
        best_move = None
        best_val = -sys.maxsize - 1
        # for each move, find minimax value and if greater than the best val,
        # change the best move and best val to this current move and value
        if len(lmoves) > 20:
            max_d = 3
        else:
            max_d = 5
        for move in lmoves:
            curr_val = self.minimax(move, pos, 1, max_d, True, self.minval, self.maxval)
            if curr_val > best_val:
                best_move = move
                best_val = curr_val
        self.log.write(str(best_move)+"\n")
        self.log.flush()
        return best_move

    # returns minimax value of a move
    def minimax(self, move, pos, depth, max_depth, my_turn, a, b):
        # if my turn, max
        # TODO check depth condition and if not met, use heuristic
        if depth == max_depth:
            # heuristic: return number of boards won by whoever's turn it is
            return pos.sum_heuristics(self.myid, self.oppid)

        # if game is won, return appropriate value
        winner = pos.checkMacroboardWinner()
        if winner != 0:
            return pos.sum_heuristics(self.myid, self.oppid)

        # make a copy of the current position so we can make moves on it
        pos_copy = copy.deepcopy(pos)
        # get the legal next moves from this position
        lmoves = pos_copy.legal_moves()

        # if no legal moves, i.e. at a terminal node, return num of boards won
        # by player whose turn it is
        if lmoves == []:
            return pos_copy.sum_heuristics(self.myid, self.oppid)

        # for each of these possible next moves, make the move using pos copy
        pos_copy.make_move(move[0], move[1], self.myid)
        if my_turn:
            started = False
            for l in lmoves:
                # set value to
                val = self.minimax(l, pos_copy, depth+1, max_depth, False, max(a, self.minval),b)
                if val >= b:
                    return self.minval
                if not started:
                    best_val = val
                else:
                    best_val = max(val, best_val)
                    started = True
            return best_val

        else:
            started = False
            for l in lmoves:
                # set value to
                val = self.minimax(l, pos_copy, depth+1, max_depth, True, a, min(b, self.maxval))
                if val <= a:
                    return self.maxval
                if not started:
                    best_val = val
                else:
                    best_val = min(val, best_val)
                    started = True
            return best_val

        # otherwise if other turn, min
