import neat
import time
import os
import sys
from fcntl import fcntl, F_GETFL, F_SETFL

training_bots = ["tictactoe-starterbot-python3"]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        eval_genome(genome, config)

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    num_reps = 20
    cumulative_fitness = 0
    for bot in training_bots:
        for _ in range(num_reps):
            result = play_game(net, bot, False)
            cumulative_fitness = cumulative_fitness + fitness(result, False)
    genome.fitness  = cumulative_fitness / len(training_bots * cumulative_fitness)

def fitness(game_res, is_first):
    #cases based on win status
    if game_res[0] == 0:
        return 0
    elif game_res[0] == 1: #player 1 wins
        if is_first:
            return 1
        else:
            return 0
    elif game_res[0] == 2: #player 2 wins
        if is_first:
            return 0
        else:
            return 1
    else:
        return 0

#play game with net being the net we are testing and bot the AI we are testing against
def play_game(net, bot_path, is_first):
    connection = EngineConnector(bot_path, is_first)
    win_status = connection.win_status()
    num_turns = 0
    # while win condition hasn't been met, loop
    while (win_status == -1):
        # read state of game
        state = connection.read_state()
        # get move from net
        #move = get_move_from_net(net, state[0])
        
        #TODO: REMOVE temporary auto-select 1st legal move
        import ast
        move = ast.literal_eval(state[2])[0]

        # send the move
        connection.send_move(str(move))
        num_turns += 1
        win_status = connection.win_status()
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
    nn_input = []*198
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
            nn_input[162+27+i] = 0
        elif mboard_s[i] == "m":
            nn_input[162+i] = 1
            nn_input[162+9+i] = 0
            nn_input[162+18+i] = 0
            nn_input[162+27+i] = 0
        elif mboard_s[i] == "d":
            nn_input[162+i] = 0
            nn_input[162+9+i] = 0
            nn_input[162+18+i] = 1
            nn_input[162+27+i] = 0
        else:
            nn_input[162+i] = 0
            nn_input[162+9+i] = 0
            nn_input[162+18+i] = 0
            nn_input[162+27+i] = 1
    nn_output = net.activate(nn_input)
    moves = range(0,81)
    moves = sorted(moves, key=lambda x:nn_output[x], reverse=True)
    for i in range(0,81):
        if check_move_legal(state[3], (moves[i]%9, moves[i]//9)):
            return (moves[i]%9, moves[i]//9)
    assert False

class EngineConnector:
    def __init__(self, otherbot_path, is_first):
        import uuid
        import subprocess
        from filelock import FileLock
        self.str_uuid = str(uuid.uuid1())
        self.interface_pipe_path = "pipes/" + self.str_uuid + ".pipe"
        self.interface_lock_path = self.interface_pipe_path + ".lock"
        self.lock = FileLock(self.interface_lock_path)
        self.is_first = is_first

        #create pipe file if it does not exist
        pipe = open(self.interface_pipe_path, "w+")
        pipe.close()

        #run engine
        otherbot_launch_str = "python3 .."+ os.sep + otherbot_path + os.sep +"main.py"
        ibot_launch_str = "python3 .."+ os.sep +"EngineInterface"+ os.sep +"main.py " + os.path.abspath(self.interface_pipe_path)

        if is_first:
            engine_launch_str = "java -cp bin com.theaigames.tictactoe.Tictactoe \""+ ibot_launch_str +"\" \"" + otherbot_launch_str + "\""
        else:
            engine_launch_str = "java -cp bin com.theaigames.tictactoe.Tictactoe \""+ otherbot_launch_str +"\" \"" + ibot_launch_str + "\""
        self.engine_process = subprocess.Popen(engine_launch_str, shell=True, stdout=subprocess.PIPE, cwd=".."+ os.sep +"ultimatetictactoe-engine")
        #avoid blocking by setting flags
        flags = fcntl(self.engine_process.stdout, F_GETFL)
        fcntl(self.engine_process.stdout, F_SETFL, flags | os.O_NONBLOCK)

    def read_state(self):
        received = ""
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
                    received = pipe.read()
                    print(received) #TODO: Remove this line
                    pipe.close()
                pipe.close()
            finally:
                self.lock.release()
            #sleep for a duration to give time for selection to be made
            time.sleep(0.001)

        #process received into a tuple of board, macroboard, moves
        lines = received.splitlines(keepends=False)
        print("state: " + str((lines[1], lines[3], lines[5])))
        return (lines[1], lines[3], lines[5])

    def send_move(self, selection):
        self.lock.acquire()
        try:
            pipe = open(self.interface_pipe_path, "w+")
            pipe.write("move\n")
            pipe.write(selection)
            pipe.close()
        finally:
            self.lock.release()

    # return 0 if draw, 1 if player 1 wins, 2 if player 2 wins, -1 if active game
    def win_status(self):
        l = self.engine_process.stdout.readline().decode(sys.getdefaultencoding())
        while l != '':
            if "Draw" in l:
                return 0
            if "winner: player1" in l:
                return 1
            if "winner: player2" in l:
                return 2
            l = self.engine_process.stdout.readline().decode(sys.getdefaultencoding())
        return -1

    def close(self):
        os.remove(self.interface_pipe_path)
        if os.path.exists(self.interface_lock_path):
            os.remove(self.interface_lock_path)

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

    checkpointer = neat.Checkpointer(generation_interval=1000)
    p.add_reporter(checkpointer)

    # Run for up to 300 generations.
    pe = neat.ParallelEvaluator(4, eval_genome)
    #winner = p.run(pe.evaluate, 10000)
    winner = p.run(eval_genomes, 10000)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # write the most fit nn
    #winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    #checkpointer.save_checkpoint(config, p, checkpointer.current_generation)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    if not os.path.exists("pipes" + os.sep):
        os.makedirs("pipes" + os.sep)
    run(config_path)