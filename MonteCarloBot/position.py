
class Position:
    
    def __init__(self):
        self.board = []
        self.macroboard = []
        self.mMacroboard = [[]]
        self.mLastX = -1
        self.mLastY = -1
    
    def parse_field(self, fstr):
        flist = fstr.replace(';', ',').split(',')
        self.board = [ int(f) for f in flist ]
    
    def parse_macroboard(self, mbstr):
        mblist = mbstr.replace(';', ',').split(',')
        self.macroboard = [ int(f) for f in mblist ]
    
    def is_legal(self, x, y):
        mbx, mby = x/3, y/3
        return self.macroboard[3*mby+mbx] == -1 and self.board[9*y+x] == 0

    def legal_moves(self):
        return [ (x, y) for x in range(9) for y in range(9) if self.is_legal(x, y) ]
        
    def make_move(self, x, y, pid):
        mbx, mby = x/3, y/3
        self.macroboard[3*mby+mbx] = -1
        self.board[9*y+x] = pid
        
    def get_board(self):
        return str.join(",", [str(i) for i in self.board])

    def get_macroboard(self):
        return str.join(",", [str(i) for i in self.macroboard])

    #from theAIGames engine
    def microboardFull(self, x, y):
        if x < 0 or y < 0:
            return True
        if (self.mMacroboard[x][y] == 1 or self.mMacroboard[x][y] == 2):
            return True
        for my in range(y*3, y*3+3):
            for mx in range(x*3, x*3+3):
                if (self.board[mx*9+my] == 0):
                    return False
        return True

    def updateMacroboard(self):
        for x in range(0, 3):
            for y in range(0, 3):
                winner = self.getMicroboardWinner(x, y)
                self.mMacroboard[x][y] = winner
        if (not self.microboardFull(self.mLastX%3, self.mLastY%3)):
            self.mMacroboard[self.mLastX%3][self.mLastY%3] = -1
        else:
            for x in range(0, 3):
                for y in range(0, 3):
                    if (not self.microboardFull(x, y)):
                        self.mMacroboard[x][y] = -1

    def getMicroboardWinner(self, macroX, macroY):
        startX = macroX*3
        startY = macroY*3
        for y in range(startY, startY+3):
            if (self.board  [startX*9+y] == self.board  [(startX+1)*9+y] and self.board  [(startX+1)*9+y] == self.board  [(startX+2)*9+y] and self.board  [(startX)*9+y] > 0):
                return self.board  [startX*9+y]
        for x in range(startX, startX+3):
            if (self.board  [x*9+startY] == self.board  [x*9+startY+1] and self.board  [x*9+startY+1] == self.board  [x*9+startY+2] and self.board  [x*9+startY] > 0):
                return self.board  [x*9+startY]
        if (self.board  [startX*9+startY] == self.board  [(startX+1)*9+startY+1] and self.board  [(startX+1)*9+startY+1] == self.board  [(startX+2)*9+startY+2] and self.board  [startX*9+startY] > 0):
            return self.board  [startX*9+startY]
        if (self.board  [(startX+2)*9+startY] == self.board  [(startX+1)*9+startY+1] and self.board  [(startX+1)*9+startY+1] == self.board  [startX*9+startY+2] and self.board  [(startX+2)*9+startY] > 0):
            return self.board  [(startX+2)*9+startY]
        return 0

    def checkMacroboardWinner(self):
        for y in range(0, 3):
            if (self.mMacroboard[0][y] == self.mMacroboard[1][y] and self.mMacroboard[1][y] == self.mMacroboard[2][y] and self.mMacroboard[0][y] > 0):
                return self.mMacroboard[0][y]
        for x in range(0, 3):
            if (self.mMacroboard[x][0] == self.mMacroboard[x][1] and self.mMacroboard[x][1] == self.mMacroboard[x][2] and self.mMacroboard[x][0] > 0):
                return self.mMacroboard[x][0]
        if (self.mMacroboard[0][0] == self.mMacroboard[1][1] and self.mMacroboard[1][1] == self.mMacroboard[2][2] and self.mMacroboard[0][0] > 0):
            return self.mMacroboard[0][0]
        if (self.mMacroboard[2][0] == self.mMacroboard[1][1] and self.mMacroboard[1][1] == self.mMacroboard[0][2] and self.mMacroboard[2][0] > 0):
            return self.mMacroboard[2][0]
        return 0