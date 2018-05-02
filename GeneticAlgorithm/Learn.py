import neat
import time
from filelock import FileLock

training_bots = []

#play game with net being the net we are testing and bot the AI we are testing against
def play_game(net, bot):
    raise NotImplementedError

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        cumulative_fitness = 0
        for bot in training_bots:
            result = play_game(net, bot)
            cumulative_fitness = cumulative_fitness #+ fitness(result)
        genome.fitness  = cumulative_fitness / len(training_bots)

class EngineConnector:
    def __init__(self):
        import uuid
        self.str_uuid = str(uuid.uuid1)
        self.interface_pipe_path = self.str_uuid + '_pipe'
        self.interface_lock_path = self.str_uuid + '_pipe.lock'
        self.ibot_launch_str = "python EngineInterface/main.py"
        self.lock = FileLock(self.interface_lock_path)
        

def send_move(selection, connector):
    #result read phase; must check that result has been written
    received_selection = False
    while (not received_selection):
        #try to read selection
        connector.lock.acquire()
        try:
            pipe = open(connector.interface_pipe_path, "r+")
            
            #check that file has been updated
            first_line = pipe.readline()
            expected = "sent"
            if (expected in first_line):
                received_selection = True
                print(pipe.read())
                pipe.close()

            pipe.close()
        finally:
            connector.lock.release()

        #sleep for a duration to give time for selection to be made
        time.sleep(0.001)

    #write phase
    connector.lock.acquire()
    try:
        pipe = open(connector.interface_pipe_path, "w+")
        pipe.write("response\n")
        pipe.write(input("Enter text: "))
        print("\n")
        
        pipe.close()
    finally:
        connector.lock.release()