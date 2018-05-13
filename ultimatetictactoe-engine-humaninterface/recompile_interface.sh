#!/usr/bin/env bash

mkdir bin
javac -d bin/ `find ./ -name '*.java' -regex '^[./A-Za-z0-9]*$'`

