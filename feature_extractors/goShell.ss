#!/bin/bash

################################################
# This program runs a topic model on the data  #
# and outputs a file containing one vector for #
# each document, with each entry of the vector #
# representing that document's probability of  #
# corresponding with a given topic             #
#                                              #
# The topics are labeled in the first line of  #
# the output file testSetWithTopics.csv        #
#                                              #
# The program takes in 2 arguments:            #
# 1. the file containing the test set data     #
# 2. the file containing the test set's labels #
################################################

cp $1 Data/testSet.dat
cp $2 Data/testSetLabels.dat

python Data/makeTestCSV.py Data/testSet.dat Data/testSet.csv

java -Xmx4096m -jar tmt-0.4.0.jar inferTopics.scala

python findMedian.py model/testSet-document-topic-distributuions.csv model/testSet-features-with-median.csv

python Data/addLabels.py model/testSet-features-with-median.csv Data/testSetLabels.dat Data/testSet.csv testSetWithTopics.csv
