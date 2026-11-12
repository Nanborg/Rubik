#!/bin/sh

scramble=$(./scramble.py)

echo "scramble:" $scramble
./rubik "$scramble" | ./render.py "$scramble"