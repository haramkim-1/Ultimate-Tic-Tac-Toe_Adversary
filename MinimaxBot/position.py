
class Position:

    def __init__(self):
        self.board = []
        self.macroboard = []

    def parse_field(self, fstr):
        flist = fstr.replace(';', ',').split(',')
        self.board = [int(f) for f in flist]

    def parse_macroboard(self, mbstr):
        mblist = mbstr.replace(';', ',').split(',')
        self.macroboard = [int(f) for f in mblist]

    def is_legal(self, x, y):
        mbx, mby = x // 3, y // 3
        return self.macroboard[3*mby+mbx] == -1 and self.board[9*y+x] == 0

    def legal_moves(self):
        return [(x, y) for x in range(9) for y in range(9)
                if self.is_legal(x, y)]

    def make_move(self, x, y, pid):
        mbx, mby = x//3, y//3
        next_mbx, next_mby = x%3, y%3
        self.board[9*y+x] = pid
        self.macroboard[3*mby+mbx] = self.getMicroboardWinner(mbx, mby)
        if self.microboardFull(mbx, mby):
            for macroX in range(0,2):
                for macroY in range(0,2):
                    if not self.microboardFull(macroX, macroY):
                        self.macroboard[3*macroY + macroX] = -1
        else:
            for macroX in range(0,2):
                for macroY in range(0,2):
                    if self.macroboard[3*macroY+macroX] == -1:
                        self.macroboard[3*macroY + macroX] = 0
            self.macroboard[3*next_mbx + next_mby] = -1

    def get_board(self):
        return str.join(",", [str(i) for i in self.board])

    def get_macroboard(self):
        return str.join(",", [str(i) for i in self.macroboard])

    # from theAIGames engine
    def microboardFull(self, x, y):
        if x < 0 or y < 0:
            return True
        if (self.macroboard[y*3+x] == 1 or self.macroboard[y*3+x] == 2):
            return True
        for my in range(y*3, y*3+3):
            for mx in range(x*3, x*3+3):
                if (self.board[my*9+mx] == 0):
                    return False
        return True

    # return number of microboards won by me if my_turn is true and number of
    # microboards won by opponent if my_turn is false
    #TODO: this counts draws as wins for the opponent
    def num_boards_won(self, myid, my_turn):
        won = 0
        for x in range(0, 2):
            for y in range(0, 2):
                if self.getMicroboardWinner(x, y) == myid and my_turn:
                    won += 1
                if self.getMicroboardWinner(x, y) != myid and not my_turn:
                    won += 1
        return won

    def getMicroboardWinner(self, macroX, macroY):
        startY = macroY*3
        startX = macroX*3
        for x in range(startX, startX+3):
            if (self.board[startY*9+x] == self.board[(startY+1)*9+x] and
                    self.board[(startY+1)*9+x] == self.board[(startY+2)*9+x]
                    and self.board[(startY)*9+x] > 0):
                return self.board[startY*9+x]
        for y in range(startY, startY+3):
            if (self.board[y*9+startX] == self.board[y*9+startX+1] and
                    self.board[y*9+startX+1] == self.board[y*9+startX+2] and
                    self.board[y*9+startX] > 0):
                return self.board[y*9+startX]
        if (self.board[startY*9+startX] == self.board[(startY+1)*9+startX+1]
                and self.board[(startY+1)*9+startX+1] ==
                self.board[(startY+2)*9+startX+2] and
                self.board[startY*9+startX] > 0):
            return self.board[startY*9+startX]
        if(self.board[(startY+2)*9+startX] == self.board[(startY+1)*9+startX+1]
                and self.board[(startY+1)*9+startX+1] ==
                self.board[startY*9+startX+2]
                and self.board[(startY+2)*9+startX] > 0):
            return self.board[(startY+2)*9+startX]
        return 0

    def checkMacroboardWinner(self):
        for x in range(0, 3):
            if (self.macroboard[x] == self.macroboard[1*3+x] and
                    self.macroboard[1*3+x] == self.macroboard[2*3+x] and
                    self.macroboard[0*3+x] > 0):
                return self.macroboard[0*3+x]
        for y in range(0, 3):
            if (self.macroboard[y*3+0] == self.macroboard[y*3+1] and
                    self.macroboard[y*3+1] == self.macroboard[y*3+2] and
                    self.macroboard[y*3+0] > 0):
                return self.macroboard[x*3+0]
        if (self.macroboard[0*3+0] == self.macroboard[1*3+1] and
                self.macroboard[1*3+1] == self.macroboard[2*3+2] and
                self.macroboard[0*3+0] > 0):
            return self.macroboard[0*3+0]
        if (self.macroboard[2*3+0] == self.macroboard[1*3+1] and
                self.macroboard[1*3+1] == self.macroboard[0*3+2] and
                self.macroboard[2*3+0] > 0):
            return self.macroboard[2*3+0]
        return 0
    
    def getMicroboardHeuristic(self, macroX, macroY, myid, oppid):
        startX = macroX*3
        startY = macroY*3
        #implement heuristic from russel and norvig
        #the perspective in writing is that myid is X, but works either way
        X1 = 0
        X2 = 0
        O1 = 0
        O2 = 0
        xcount = 0
        ocount = 0
        #check horizontal rows
        for x in range(startX, startX+3):
            for y in range(startY, startY+3):
                if self.board[9*y+x] == myid:
                    xcount = xcount + 1
                elif self.board[9*y+x] == oppid:
                    ocount = ocount + 1
            if ocount == 0:
                if xcount == 1:
                    X1 = X1 + 1
                elif xcount == 2:
                    X2 = X2 + 1
                elif xcount == 3:
                    return 15
            if xcount == 0:
                if ocount == 1:
                    O1 = O1 + 1
                elif ocount == 2:
                    O2 = O2 + 1
                elif ocount == 3:
                    return -15
            xcount = 0
            ocount = 0
        #check vertical rows
        for y in range(startY, startY+3):
            for x in range(startX, startX+3):
                if self.board[9*y+x] == myid:
                    xcount = xcount + 1
                elif self.board[9*y+x] == oppid:
                    ocount = ocount + 1
            if ocount == 0:
                if xcount == 1:
                    X1 = X1 + 1
                elif xcount == 2:
                    X2 = X2 + 1
                elif xcount == 3:
                    return 15
            if xcount == 0:
                if ocount == 1:
                    O1 = O1 + 1
                elif ocount == 2:
                    O2 = O2 + 1
                elif ocount == 3:
                    return -15
            xcount = 0
            ocount = 0
        #check diagonals
        for i in range(0, 3):
            if self.board[9*(i + startY)+(i + startX)] == myid:
                 xcount = xcount + 1
            elif self.board[9*(i + startY)+(i + startX)] == oppid:
                ocount = ocount + 1
        if ocount == 0:
            if xcount == 1:
                X1 = X1 + 1
            elif xcount == 2:
                X2 = X2 + 1
            elif xcount == 3:
                return 15
        if xcount == 0:
            if ocount == 1:
                O1 = O1 + 1
            elif ocount == 2:
                O2 = O2 + 1
            elif ocount == 3:
                return -15
        xcount = 0
        ocount = 0
        for i in range(0, 3):
            if self.board[9*(2 - i + startY)+(i + startX)] == myid:
                 xcount = xcount + 1
            elif self.board[9*(2 - i + startY)+(i + startX)] == oppid:
                ocount = ocount + 1
        if ocount == 0:
            if xcount == 1:
                X1 = X1 + 1
            elif xcount == 2:
                X2 = X2 + 1
            elif xcount == 3:
                return 15
        if xcount == 0:
            if ocount == 1:
                O1 = O1 + 1
            elif ocount == 2:
                O2 = O2 + 1
            elif ocount == 3:
                return -15
        #calculate final heuristic
        return 3*X2 + X1 - 3*O2 - O1

    def sum_heuristics(self, myid, oppid):
        total = 0
        for x in range(0,3):
            for y in range(0,3):
                total = total + self.getMicroboardHeuristic(x, y, myid, oppid)
        return total