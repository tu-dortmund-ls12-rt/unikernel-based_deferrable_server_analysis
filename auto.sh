#!/usr/bin/env bash

# different utilizations
python3 main.py -s1 -u 0.1:0.1
python3 main.py -s1 -u 0.2:0.2
python3 main.py -s1 -u 0.3:0.3
python3 main.py -s1 -u 0.4:0.4
python3 main.py -s3

# different number of servers per system
python3 main.py -s1 -n 10:10
python3 main.py -s1 -n 50:50
python3 main.py -s1 -n 100:100
python3 main.py -s2