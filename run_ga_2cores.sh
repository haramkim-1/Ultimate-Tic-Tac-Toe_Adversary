#!/usr/bin/env bash
cd GeneticAlgorithm

taskset --cpu-list 1,2 python Learn.py #2>ga_error_log.txt 1>ga_stdout_log.txt

cd ..
