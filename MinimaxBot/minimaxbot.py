class MinimaxBot:

    def get_move(self, pos, tleft):
        lmoves = pos.legal_moves()
        # TODO: initialize this to the first move in lmoves?
        best_move = None
        # TODO: find a good initial value
        best_val = None
        # for each move, find minimax value and if greater than the best val,
        # change the best move and best val to this current move and value
        for move in lmoves:
            curr_val = minimax(move, pos, 1, 3, True)
            if curr_val > best_val
                best_move = move
                best_val = curr_val
        return best_move

    def minimax(move, pos, depth, max_depth, my_turn):

        # if my turn, max
        # TODO check depth condition and if not met, use heuristic
        if depth == max_depth:
            # heuristic : return the number of boards won by whoever's turn it is
            return pos.num_boards_won(self.myid, my_turn)

        # make a copy of the current position so we can make moves on it
        pos_copy = copy.deepcopy(pos)
        # get the legal next moves from this position
        lmoves = pos_copy.legal_moves()

        if lmoves == []:
            

        # for each of these possible next moves, make the move using pos copy
        make_move(pos_copy, move[0], move[1], self.myid)

        if my_turn:
            started = false
            for l in lmoves:
                # set value to
                val = minimax(l, pos_copy, depth+1, max_depth, False)
                if not started:
                    best_val = val
                else:
                    best_val = max(val, best_val)
                    started = True
            return best_val

        else:
            started = false
            for l in lmoves:
                # set value to
                val = minimax(l, pos_copy, depth+1, max_depth, True)
                if not started:
                    best_val = val
                else:
                    best_val = min(val, best_val)
                    started = True
            return best_val

        # otherwise if other turn, min
