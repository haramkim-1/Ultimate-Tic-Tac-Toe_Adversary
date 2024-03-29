import neat
import time
import os
import sys
import pickle
from time import gmtime, strftime
from fcntl import fcntl, F_GETFL, F_SETFL


debug=False#turn off for real run
if debug:
    training_bots = [("python3 .." + os.sep + "tictactoe-starterbot-python3/main.py", 1, 1), ("python3 .." + os.sep + "NNBot/main.py ../networks/versus_random_winner.pickle", 1, 10), ("java -Duser.dir=.."+os.sep+"external_javabot"+os.sep+"bin BotStarter", 1, 15)]
else:
    #training_bots = ["tictactoe-starterbot-python3", "MonteCarloBot"]
    training_bots = [("python3 .." + os.sep + "tictactoe-starterbot-python3/main.py", 30, 1), ("python3 .." + os.sep + "NNBot/main.py ../networks/versus_minimax_external_winner.pickle", 1, 2), ("python3 .." + os.sep + "NNBot/main.py ../networks/versus_random_winner.pickle", 1, 2), ("java -Duser.dir=.."+os.sep+"external_javabot"+os.sep+"bin BotStarter", 1, 2)]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    cumulative_fitness = 0
    game_count = 0
    for bot,reps,weight in training_bots:
        for _ in range(reps):
            result = play_game(net, bot, False)
            game_count += (1 * weight)
            cumulative_fitness += fitness(result, False) * weight
    fitness_float = cumulative_fitness / game_count
    assert isinstance(fitness_float, float)
    return fitness_float

def fitness(game_res, is_first):
    #cases based on win status
    if game_res[0] == 0: #draw
        return 0
    elif game_res[0] == 1: #player 1 wins
        if is_first:
            return 1
        else:
            return 0 + game_res[1]/80
    elif game_res[0] == 2: #player 2 wins
        if is_first:
            return 0 + game_res[1]/80
        else:
            return 1
    else:
        return 0

#play game with net being the net we are testing and bot the AI we are testing against
def play_game(net, bot_path, is_first):
    connection = EngineConnector(bot_path, is_first)
    num_turns = 0
    win_status = -1
    win_status = connection.win_status()
    try:
       # win_status = connection.win_status()
        # while win condition hasn't been met, loop
        while (win_status == -1):
            #print("turn: " + str(num_turns))
            # read state of game
            state = None
            while(state == None and connection.engine_process.poll() == None):
                state = connection.try_read_state()
            #print("state read")
            #if failed to read state, update win_status and break
            if state == None:
                #print("exiting")
                win_status = connection.win_status()
                break
            # get move from net
            move = get_move_from_net(net, state)
            
            #TODO: REMOVE temporary auto-select 1st legal move
            #import ast
            #move = ast.literal_eval(state[2])[0]

            # send the move
            connection.send_move(str(move))
            num_turns += 1
            #print("move sent")

            win_status = connection.win_status()
    finally:
        connection.close()
    return win_status, num_turns

# will extract new move
def check_move_legal(moves_str, move):
    return str(move) in moves_str

# should return a move in the form (x,y)
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
    
    #move legality check for 1st 10
    for i in range(0,10):
        if check_move_legal(state[2], (moves[i]%9, moves[i]//9)):
            return (moves[i]%9, moves[i]//9)
    return (moves[0]%9, moves[0]//9)


class EngineConnector:
    def __init__(self, otherbot_path, is_first):
        import uuid
        import subprocess
        from filelock import FileLock
        self.str_uuid = str(uuid.uuid1())
        self.interface_pipe_path = os.path.abspath("pipes"+ os.sep + self.str_uuid + ".pipe")
        self.interface_lock_path = self.interface_pipe_path + ".lock"
        self.lock = FileLock(self.interface_lock_path)
        self.is_first = is_first

        #create pipe file
        #os.mknod(os.path.abspath(self.interface_pipe_path))
        pipe = open(self.interface_pipe_path, "w+")
        pipe.close()

        #run engine
        ibot_launch_str = "python3 .."+ os.sep +"EngineInterface"+ os.sep +"main.py " + self.interface_pipe_path

        if is_first:
            engine_launch_str = "java -cp bin com.theaigames.tictactoe.Tictactoe \""+ ibot_launch_str +"\" \"" + otherbot_path + "\""
        else:
            engine_launch_str = "java -cp bin com.theaigames.tictactoe.Tictactoe \""+ otherbot_path +"\" \"" + ibot_launch_str + "\""
        self.engine_process = subprocess.Popen(engine_launch_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=".."+ os.sep +"ultimatetictactoe-engine")
        #avoid blocking by setting flags
        flags = fcntl(self.engine_process.stdout, F_GETFL)
        fcntl(self.engine_process.stdout, F_SETFL, flags | os.O_NONBLOCK)
        fcntl(self.engine_process.stderr, F_SETFL, flags | os.O_NONBLOCK)

    def read_state(self):
        #print("reading state")
        received = ""
        received_selection = False
        while (not received_selection):
            #try to read selection
            self.lock.acquire()
            try:
                pipe = open(self.interface_pipe_path, "r")
                #check that file has been updated
                first_line = pipe.readline()
                expected = "state"
                if (expected in first_line):
                    received_selection = True
                    received = pipe.read()
                    pipe.close()
                pipe.close()
            finally:
                self.lock.release()
            #sleep for a duration to give time for selection to be made
            time.sleep(0.001)
        #process received into a tuple of board, macroboard, moves
        lines = received.splitlines(keepends=False)
        #print("state: " + str((lines[1], lines[3], lines[5])))
        return (self.process_board(lines[1]), self.process_macroboard(lines[3]), lines[5])

    #attempts a single state read
    def try_read_state(self):
        received = ""
        received_selection = False
        self.lock.acquire()
        try:
            pipe = open(self.interface_pipe_path, "r")
            #check that file has been updated
            first_line = pipe.readline()
            expected = "state"
            if (expected in first_line):
                received_selection = True
                received = pipe.read()
                pipe.close()
            pipe.close()
        finally:
            self.lock.release()
        if received_selection:
            lines = received.splitlines(keepends=False)
            #print("state: " + str((lines[1], lines[3], lines[5]))) 
            return (self.process_board(lines[1]), self.process_macroboard(lines[3]), lines[5])
        else:
            return None
        
    
    def send_move(self, selection):
        self.lock.acquire()
        try:
            pipe = open(self.interface_pipe_path, "w+")
            pipe.write("move\n")
            pipe.write(selection)
            pipe.close()
        finally:
            self.lock.release()

    def process_board(self, pre_board):
        if self.is_first:
            return pre_board.replace("-1","a").replace("1","m").replace("2","y").replace("a","-1")
        else:
            return pre_board.replace("-1","a").replace("2","m").replace("1","y").replace("a","-1")

    def process_macroboard(self, pre_macroboard):
        if self.is_first:
            return pre_macroboard.replace("-1","a").replace("1","m").replace("2","y").replace("a","-1")
        else:
            return pre_macroboard.replace("-1","a").replace("2","m").replace("1","y").replace("a","-1")

    # return 0 if draw, 1 if player 1 wins, 2 if player 2 wins, -1 if active game
    def win_status(self):
        l = self.engine_process.stdout.readline().decode(sys.getdefaultencoding())
        while l != "":
            #print("l:" + l)
            if "Draw" in l:
                return 0
            if "winner: player1" in l:
                return 1
            if "winner: player2" in l:
                return 2
            l = self.engine_process.stdout.readline().decode(sys.getdefaultencoding())
        return -1

    def close(self):
        if os.path.exists(self.interface_lock_path):
            os.remove(self.interface_lock_path)
        os.remove(self.interface_pipe_path)

def pickle_winner_net(net):
    time_str = strftime("%Y-%m-%d-%H-%M", gmtime())
    pickle_file = open(time_str + "_winner.pickle", "wb+")
    pickle.dump(net, pickle_file)
    pickle_file.close()

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    checkpointer = neat.Checkpointer(generation_interval=50)
    p.add_reporter(checkpointer)

    # Run for up to 300 generations.
    if debug:
        pe = neat.ParallelEvaluator(2, eval_genome)
        winner = p.run(pe.evaluate, 1)
    else:
        pe = neat.ParallelEvaluator(30, eval_genome)
        winner = p.run(pe.evaluate, 1000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # write the most fit nn
    checkpointer.save_checkpoint(config, p, winner, checkpointer.current_generation)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    pickle_winner_net(winner_net)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    print("running with niceness: " + str(os.nice(10)))
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    if not os.path.exists("pipes" + os.sep):
        os.makedirs("pipes" + os.sep)
    run(config_path)