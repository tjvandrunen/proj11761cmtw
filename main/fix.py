#!/usr/bin/python

import sys

test_data = open(sys.argv[1]).readlines()
train_data = open("./Data/train.csv").readlines()

if test_data[1].split(',')[0] == "TRUE":
	del train_data[1]

f = open("./Data/train.csv",'w')

for line in train_data:
	f.write(line)
f.close()
