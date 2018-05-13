#!/usr/bin/env bash

#java -cp bin com.theaigames.tictactoe.Tictactoe "python3 ../MinimaxBot/main.py" "python3 ../tictactoe-starterbot-python3/main.py"

java -cp bin com.theaigames.tictactoe.Tictactoe "python3 ../MinimaxBot/main.py" "java -Duser.dir=../external_javabot/bin BotStarter"
