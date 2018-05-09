import neat

class NeuralNetworkBot:

    def __init__(self, net):
        self.neuralnet = net
        self.order_detected = False #flag for if we've already found the order
        self.is_first = False #default value, not known at this point
    
    def get_move(self, pos, tleft):
        lmoves = pos.legal_moves()
        #state tuple in style used by Learn
        state_strs = (process_board(self.is_first, str(pos.get_board())), process_macroboard(self.is_first, str(pos.get_macroboard())), str(lmoves))
        #raise Exception(str(state_strs))
        #find if we're first if not already detected
        if not self.order_detected:
            self.order_detected = True
            self.is_first = not ("1" in state_strs[0]) #will contain 1 if 2nd
        #extract move from nn
        nn_move = get_move_from_net(self.neuralnet, state_strs)
        #pick move from lmoves
        lmoves_strings = [str(x) for x in lmoves]
        return lmoves[lmoves_strings.index(nn_move)]

#function transposed from Learn; extracts move from the neural network
def get_move_from_net(net, state):
    board_state = state[0]
    macroboard_state = state[1]
    board_moves = board_state.split(",")
    nn_input = [0]*189
    for i in range(0,81):
        if board_moves[i] == "y":
            nn_input[i] = 0
            nn_input[i+81] = 1
        elif board_moves[i] == "m":
            nn_input[i] = 1
            nn_input[i+81] = 0
        else:
            nn_input[i] = 0
            nn_input[i+81] = 0
    mboard_s = macroboard_state.split(",")
    for i in range(0,9):
        if mboard_s[i] == "y":
            nn_input[162+i] = 0
            nn_input[162+9+i] = 1
            nn_input[162+18+i] = 0
        elif mboard_s[i] == "m":
            nn_input[162+i] = 1
            nn_input[162+9+i] = 0
            nn_input[162+18+i] = 0
        elif mboard_s[i] == "-1":
            nn_input[162+i] = 0
            nn_input[162+9+i] = 0
            nn_input[162+18+i] = 1
    nn_output = net.activate(nn_input)
    moves = range(0,81)
    moves = sorted(moves, key=lambda x:nn_output[x], reverse=True)
    for i in range(0,81):
        if check_move_legal(state[2], (moves[i]%9, moves[i]//9)):
            return (moves[i]%9, moves[i]//9)
    assert False

#also transposed from Learn
def check_move_legal(moves_str, move):
    return str(move) in moves_str

def process_board(first, pre_board):
        if first:
            return pre_board.replace("-1","a").replace("1","m").replace("2","y").replace("a","-1")
        else:
            return pre_board.replace("-1","a").replace("2","m").replace("1","y").replace("a","-1")

def process_macroboard(first, pre_macroboard):
    if first:
        return pre_macroboard.replace("-1","a").replace("1","m").replace("2","y").replace("a","-1")
    else:
        return pre_macroboard.replace("-1","a").replace("2","m").replace("1","y").replace("a","-1")