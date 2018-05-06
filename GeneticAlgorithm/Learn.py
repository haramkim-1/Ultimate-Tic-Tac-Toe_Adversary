import neat
import time

training_bots = []

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    cumulative_fitness = 0
    for bot in training_bots:
        result = play_game(net, bot)
        cumulative_fitness = cumulative_fitness + fitness(result)
    genome.fitness  = cumulative_fitness / len(training_bots)

# return true if a win condition has been met in the game, and false otherwise
def win_condition_met(connection):
    while True:
        l = connection.stdout.readline()
        if "Draw!" in l or :
            return True


#play game with net being the net we are testing and bot the AI we are testing against
def play_game(net, bot_path):
    connection = EngineConnector(bot_path, False)

    # while win condition hasn't been met, loop
    # read state of game
    # get move from net
    # send the move
    raise NotImplementedError

# TODO: will extract new move
def check_move_legal(moves_str, move):

    raise NotImplementedError

# TODO: should return a move in the form (x,y)
def get_move_from_net(net, state):
    raise NotImplementedError

class EngineConnector:
    def __init__(self, otherbot_path, is_first):
        import uuid
        import subprocess
        import os
        from filelock import FileLock
        self.str_uuid = str(uuid.uuid1)
        self.interface_pipe_path = self.str_uuid + "_pipe"
        self.interface_lock_path = self.str_uuid + "_pipe.lock"
        self.lock = FileLock(self.interface_lock_path)
        self.is_first = is_first

        #create pipe file if it does not exist
        pipe = open(self.interface_pipe_path, "w+")
        pipe.close()

        #run engine
        otherbot_launch_str = "python3 .."+ os.sep + otherbot_path + os.sep +"main.py"
        ibot_launch_str = "python3 .."+ os.sep +"EngineInterface"+ os.sep +"main.py " + os.path.abspath(self.interface_pipe_path)

        if is_first:
            engine_launch_str = "java -cp bin com.theaigames.tictactoe.Tictactoe \""+ ibot_launch_str +"\" \"" + otherbot_launch_str + "\" 2>.."+ os.sep +"err.txt 1>.."+ os.sep +"out.txt"
        else:
            engine_launch_str = "java -cp bin com.theaigames.tictactoe.Tictactoe \""+ otherbot_launch_str +"\" \"" + ibot_launch_str + "\" 2>.."+ os.sep +"err.txt 1>.."+ os.sep +"out.txt"

        print("launchstr: " + engine_launch_str)
        self.engine_process = subprocess.Popen(engine_launch_str, shell=True, cwd=".."+ os.sep +"ultimatetictactoe-engine")

    def read_state(self):
        recieved = ""
        received_selection = False
        while (not received_selection):
            #try to read selection
            self.lock.acquire()
            try:
                pipe = open(self.interface_pipe_path, "r+")
                #check that file has been updated
                first_line = pipe.readline()
                expected = "state"
                if (expected in first_line):
                    received_selection = True
                    recieved = pipe.read()
                    print(recieved) #TODO: Remove this line
                    pipe.close()
                pipe.close()
            finally:
                self.lock.release()
            #sleep for a duration to give time for selection to be made
            time.sleep(0.001)

        #process recieved into a tuple of board, macroboard, moves
        lines = recieved.splitlines(keepends=False)
        return (lines[2], lines[4], lines[6])

    def send_move(self, selection):
        self.lock.acquire()
        try:
            pipe = open(self.interface_pipe_path, "w+")
            pipe.write("move\n")
            pipe.write(selection)
            pipe.close()
        finally:
            self.lock.release()
