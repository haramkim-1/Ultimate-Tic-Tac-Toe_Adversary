
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
        self.macroboard[3*mby+mbx] = -1
        self.board[9*y+x] = pid

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
        startY = macroX*3
        startX = macroY*3
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
