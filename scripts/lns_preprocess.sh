#!/bin/bash
#lns_preprocess.sh
#Weston Feely
#4/17/13
#Shell script to pre-process data sets
#The different steps are:
#(1) format the data for TurboParser
#(2) tag & parse the data with TurboParser
#(3) format the parsed data into a easily-readable tagged file, and add the document boundaries back into the parsed file

#Input args: input filename to preprocess, TurboParser-2.0.2 directory
input_filename=$1
turbo_scripts_dir=$2/scripts/

#Get start time and print current time
T="$(date +%s)"
date

#Prepare input data file for parsing
echo "Preparing ${input_filename} for parsing..."
python lns_parsing_prep.py ${input_filename} ${input_filename}.prep

#Export required library path for Turbo
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:`pwd;`/deps/local/lib:"

#Parse prepared data file
echo "Parsing ${input_filename}.prep..."
${turbo_scripts_dir}./parse.sh ${input_filename}.prep > ${input_filename}.parsed

#Create tagging formatted corpus and add document boundaries back into parsed file
echo "Creating tagged corpus from ${input_filename}.parsed and adding document boundaries back into ${input_filename}.parsed..."
python lns_tag_format.py ${input_filename} ${input_filename}.parsed ${input_filename}.tagged

#Let user know we've finished, and print time elapsed
echo "Done!"
T="$(($(date +%s)-T))"
date
printf "Time elapsed: %02d:%02d:%02d:%02d\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))"
