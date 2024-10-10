#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

cmake -S . -B build
cd build
cmake --build .