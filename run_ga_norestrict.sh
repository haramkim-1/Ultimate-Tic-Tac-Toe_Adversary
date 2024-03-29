#!/usr/bin/env bash
cd GeneticAlgorithm

DATE=$(date '+%Y-%m-%d-%H-%M')
DIR=old_checkpoints/"$DATE"
mkdir "$DIR"

echo "Full run starting at time: ""$DATE"
python -u Learn.py 2>"$DIR"/error_log.txt 1>"$DIR"/stdout_log.txt

mv neat-checkpoint-* "$DIR"
mv *.pickle "$DIR"

cd ..
