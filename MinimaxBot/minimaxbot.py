import copy
import sys


class MinimaxBot:

    myid = -1
    oppid = -1

    def get_move(self, pos, tleft):
        lmoves = pos.legal_moves()
        # TODO: initialize this to the first move in lmoves?
        best_move = None
        best_val = -sys.maxsize - 1
        # for each move, find minimax value and if greater than the best val,
        # change the best move and best val to this current move and value
        for move in lmoves:
            curr_val = self.minimax(move, pos, 1, 3, True)
            if curr_val > best_val:
                best_move = move
                best_val = curr_val
        return best_move

    # returns minimax value of a move
    def minimax(self, move, pos, depth, max_depth, my_turn):
        # if my turn, max
        # TODO check depth condition and if not met, use heuristic
        if depth == max_depth:
            # heuristic: return number of boards won by whoever's turn it is
            return pos.num_boards_won(self.myid, my_turn)

        # make a copy of the current position so we can make moves on it
        pos_copy = copy.deepcopy(pos)
        # get the legal next moves from this position
        lmoves = pos_copy.legal_moves()

        # if no legal moves, i.e. at a terminal node, return num of boards won
        # by player whose turn it is
        if lmoves == []:
            return pos_copy.num_boards_won(self.myid, my_turn)

        # for each of these possible next moves, make the move using pos copy
        pos_copy.make_move(move[0], move[1], self.myid)

        if my_turn:
            started = False
            for l in lmoves:
                # set value to
                val = self.minimax(l, pos_copy, depth+1, max_depth, False)
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
                val = self.minimax(l, pos_copy, depth+1, max_depth, True)
                if not started:
                    best_val = val
                else:
                    best_val = min(val, best_val)
                    started = True
            return best_val

        # otherwise if other turn, min
