#!/usr/bin/env bash
cd ultimatetictactoe-engine

#java -cp bin com.theaigames.tictactoe.Tictactoe "python3 ../tictactoe-starterbot-python3/main.py" "python3 ../EngineInterface/main.py ../GeneticAlgorithm/mypipe" 2>../err.txt 1>../out.txt

java -cp bin com.theaigames.tictactoe.Tictactoe "python3 ../MonteCarloBot/main.py" "python3 ../tictactoe-starterbot-python3/main.py" 2>../mc_err.txt 1>../mc_out.txt

cd ..
