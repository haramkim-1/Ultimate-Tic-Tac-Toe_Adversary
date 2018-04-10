import neat

training_bots = []

#play game with net being the net we are testing and bot the AI we are testing against
def play_game(net, bot):
    raise notImplementedError

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        cumulative_fitness = 0
        for bot in training_bots:
            result = play_game(net, bot)
            cumulative_fitness = cumulative_fitness + fitness(result)
        genome.fitness  = cumulative_fitness / len(training_bots)
