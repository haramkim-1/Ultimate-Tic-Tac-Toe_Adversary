import neat
import visualize
import os
import sys
import pickle

if __name__ == '__main__':
    pickle_path = sys.argv[1]
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         ".." + os.sep + "GeneticAlgorithm" + os.sep + 
                         "config-feedforward")
    #unpickle
    net = pickle.load(open( pickle_path, "rb" ))
    #visualize
    visualize.draw_net(config, net, True)
    