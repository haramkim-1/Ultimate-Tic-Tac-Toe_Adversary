import neat
import visualize
import os
import sys
import inspect

def fake_eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 1

if __name__ == '__main__':
    pickle_path = sys.argv[1]
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         ".." + os.sep + "GeneticAlgorithm" + os.sep + 
                         "config-feedforward")
    #load checkpoint
    checkpoint_path = sys.argv[1]
    checkpoint = neat.Checkpointer.restore_checkpoint(checkpoint_path)
    #genome = checkpoint.run(fake_eval_genomes,1)
    best = None
    best_fitness = 0.
    for k,v in checkpoint.population.population.items():
        if(v.fitness > best_fitness):
            best_fitness = v.fitness
            best = v

    #visualize
    visualize.draw_net(config, best, view=True, show_disabled=False)

    
    