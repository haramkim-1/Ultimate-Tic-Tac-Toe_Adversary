
class Position:
    
    def __init__(self):
        self.board = []
        self.macroboard = []
        self.mLastX = -1
        self.mLastY = -1
    
    def parse_field(self, fstr):
        flist = fstr.replace(';', ',').split(',')
        self.board = [ int(f) for f in flist ]
    
    def parse_macroboard(self, mbstr):
        mblist = mbstr.replace(';', ',').split(',')
        self.macroboard = [ int(f) for f in mblist ]
    
    def is_legal(self, x, y):
        mbx, mby = x//3, y//3
        return self.macroboard[3*mbx+mby] == -1 and self.board[9*x+y] == 0

    def legal_moves(self):
        return [ (x, y) for x in range(9) for y in range(9) if self.is_legal(x, y) ]
        
    def make_move(self, x, y, pid):
        self.mLastX, self.mLastY = x, y
        self.board[9*x+y] = pid
        self.updateMacroboard()
        
    def get_board(self):
        return str.join(",", [str(i) for i in self.board])

    def get_macroboard(self):
        return str.join(",", [str(i) for i in self.macroboard])

    #from theAIGames engine
    def microboardFull(self, x, y):
        if x < 0 or y < 0:
            return True
        if (self.macroboard[x*3+y] == 1 or self.macroboard[x*3+y] == 2):
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
                self.macroboard[x*3+y] = winner
        if (not self.microboardFull(self.mLastX%3, self.mLastY%3)):
            self.macroboard[self.mLastX%3*3+self.mLastY%3] = -1
        else:
            for x in range(0, 3):
                for y in range(0, 3):
                    if (not self.microboardFull(x, y)):
                        self.macroboard[x*3+y] = -1

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
            if (self.macroboard[y] == self.macroboard[1*3+y] and self.macroboard[1*3+y] == self.macroboard[2*3+y] and self.macroboard[0*3+y] > 0):
                return self.macroboard[0*3+y]
        for x in range(0, 3):
            if (self.macroboard[x*3+0] == self.macroboard[x*3+1] and self.macroboard[x*3+1] == self.macroboard[x*3+2] and self.macroboard[x*3+0] > 0):
                return self.macroboard[x*3+0]
        if (self.macroboard[0*3+0] == self.macroboard[1*3+1] and self.macroboard[1*3+1] == self.macroboard[2*3+2] and self.macroboard[0*3+0] > 0):
            return self.macroboard[0*3+0]
        if (self.macroboard[2*3+0] == self.macroboard[1*3+1] and self.macroboard[1*3+1] == self.macroboard[0*3+2] and self.macroboard[2*3+0] > 0):
            return self.macroboard[2*3+0]
        return 0