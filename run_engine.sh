#!/usr/bin/env bash
cd ultimatetictactoe-engine

java -cp bin com.theaigames.tictactoe.Tictactoe "python3 ../tictactoe-starterbot-python3/main.py" "python3 ../EngineInterface/main.py ../EngineInterface/mypipe" 2>../err.txt 1>../out.txt

cd ..
