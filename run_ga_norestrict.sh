#!/usr/bin/env bash
cd GeneticAlgorithm

DATE=$(date '+%d-%b-%Y-%H:%M')
DIR=old_checkpoints/"$DATE"
mkdir "$DIR"

python Learn.py 2>"$DIR"/error_log.txt 1>"$DIR"/stdout_log.txt

mv neat-checkpoint-*. "$DIR"

cd ..
