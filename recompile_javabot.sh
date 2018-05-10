#!/usr/bin/env bash
cd external_javabot

javac -d bin/ `find ./ -name '*.java' -regex '^[./A-Za-z0-9]*$'`

cd ..
