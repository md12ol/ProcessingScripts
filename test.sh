#!/usr/bin/env bash

echo "hello";

pwd;

javac -d out src/*.java;

java -Xms64M -Xmx2G -cp out DirTools 29;