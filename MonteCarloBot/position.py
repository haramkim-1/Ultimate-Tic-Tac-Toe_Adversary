
class Position:

    def __init__(self):
        self.board = []
        self.macroboard = []
        self.mLastX = -1
        self.mLastY = -1

    def __str__(self):
        return "Position: " + ",".join(map(lambda x:str(x),self.board))

    def parse_field(self, fstr):
        flist = fstr.replace(';', ',').split(',')
        self.board = [ int(f) for f in flist ]

    def parse_macroboard(self, mbstr):
        mblist = mbstr.replace(';', ',').split(',')
        self.macroboard = [ int(f) for f in mblist ]

    def is_legal(self, x, y):
        mbx, mby = x//3, y//3
        return self.macroboard[3*mby+mbx] == -1 and self.board[9*y+x] == 0

    def legal_moves(self):
        return [ (x, y) for x in range(9) for y in range(9) if self.is_legal(x, y) ]

    def make_move(self, move, pid):
        x, y = move
        self.mLastX, self.mLastY = move
        self.board[9*y+x] = pid
        self.updateMacroboard()

    def get_board(self):
        return str.join(",", [str(i) for i in self.board])

    def get_macroboard(self):
        return str.join(",", [str(i) for i in self.macroboard])

    #from theAIGames engine
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

    def updateMacroboard(self):
        for x in range(0, 3):
            for y in range(0, 3):
                winner = self.getMicroboardWinner(x, y)
                self.macroboard[y*3+x] = winner
        if (not self.microboardFull(self.mLastX%3, self.mLastY%3)):
            self.macroboard[self.mLastX%3*3+self.mLastY%3] = -1
        else:
            for x in range(0, 3):
                for y in range(0, 3):
                    if (not self.microboardFull(x, y)):
                        self.macroboard[y*3+x] = -1

    def getMicroboardWinner(self, macroX, macroY):
        startY = macroX*3
        startX = macroY*3
        for x in range(startX, startX+3):
            if (self.board  [startY*9+x] == self.board  [(startY+1)*9+x] and self.board  [(startY+1)*9+x] == self.board  [(startY+2)*9+x] and self.board  [(startY)*9+x] > 0):
                return self.board  [startY*9+x]
        for y in range(startY, startY+3):
            if (self.board  [y*9+startX] == self.board  [y*9+startX+1] and self.board  [y*9+startX+1] == self.board  [y*9+startX+2] and self.board  [y*9+startX] > 0):
                return self.board  [y*9+startX]
        if (self.board  [startY*9+startX] == self.board  [(startY+1)*9+startX+1] and self.board  [(startY+1)*9+startX+1] == self.board  [(startY+2)*9+startX+2] and self.board  [startY*9+startX] > 0):
            return self.board  [startY*9+startX]
        if (self.board  [(startY+2)*9+startX] == self.board  [(startY+1)*9+startX+1] and self.board  [(startY+1)*9+startX+1] == self.board  [startY*9+startX+2] and self.board  [(startY+2)*9+startX] > 0):
            return self.board  [(startY+2)*9+startX]
        return 0

    def checkMacroboardWinner(self):
        for x in range(0, 3):
            if (self.macroboard[x] == self.macroboard[1*3+x] and self.macroboard[1*3+x] == self.macroboard[2*3+x] and self.macroboard[0*3+x] > 0):
                return self.macroboard[0*3+x]
        for y in range(0, 3):
            if (self.macroboard[y*3+0] == self.macroboard[y*3+1] and self.macroboard[y*3+1] == self.macroboard[y*3+2] and self.macroboard[y*3+0] > 0):
                return self.macroboard[x*3+0]
        if (self.macroboard[0*3+0] == self.macroboard[1*3+1] and self.macroboard[1*3+1] == self.macroboard[2*3+2] and self.macroboard[0*3+0] > 0):
            return self.macroboard[0*3+0]
        if (self.macroboard[2*3+0] == self.macroboard[1*3+1] and self.macroboard[1*3+1] == self.macroboard[0*3+2] and self.macroboard[2*3+0] > 0):
            return self.macroboard[2*3+0]
        return 0
