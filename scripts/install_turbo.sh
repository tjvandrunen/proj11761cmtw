#!/bin/bash
#install_turbo.sh
#Weston Feely
#4/17/13

#This bash script will download and install TurboParser v2.0.2 in the current directory, along with the necessary model files to run English TurboTagger and TurboParser

#Download TurboParser package
wget http://www.cs.cmu.edu/~afm/TurboParser/TurboParser-2.0.2.tar.gz
#Untar archive
tar -zxvf TurboParser-2.0.2.tar.gz
#Move into Turbo folder
cd TurboParser-2.0.2
#Install
./install_deps.sh
./configure && make && make install
#Make tmp dir in scripts folder
mkdir scripts/tmp
#Move into models directory and make english_proj dir
cd models/
mkdir english_proj
#Download and untar English TurboTagger model
wget http://www.ark.cs.cmu.edu/TurboParser/sample_models/english_proj_tagger.tar.gz
tar -xvzf english_proj_tagger.tar.gz
#Download and untar English TurboParser model
wget http://www.ark.cs.cmu.edu/TurboParser/sample_models/english_proj_parser.tar.gz
tar -xvzf english_proj_parser.tar.gz
