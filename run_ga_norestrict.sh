#!/usr/bin/env bash
cd GeneticAlgorithm

python Learn.py 2>ga_error_log.txt 1>ga_stdout_log.txt &

cd ..
