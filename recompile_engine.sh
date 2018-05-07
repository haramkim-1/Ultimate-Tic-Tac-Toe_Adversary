#!/usr/bin/env bash
cd ultimatetictactoe-engine

javac -d bin/ `find ./ -name '*.java' -regex '^[./A-Za-z0-9]*$'`

cd ..
