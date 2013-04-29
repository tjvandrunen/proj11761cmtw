#!/usr/bin/python
#lns_parsing_prep.py
#Weston Feely
#4/17/13
import sys

#Prepares input data file for parsing, by removing document boundaries and sentence boundary context cues
def main(args):
    #Check for required args
    if len(args) < 3:
        print "Usage: python lns_parsing_prep.py input_file output_file"
        return 1
    #Read in filenames from args
    infile = args[1]
    outfile = args[2]
    #Loop through input file data
    out_list = []
    for line in open(infile).readlines():
        #Ignore document breaks
        if set(list(line.strip())) != set(['~']):
            #Remove context cues <s> and </s> from line
            modified = ' '.join(line.split()[1:-1])
            #Append line to output list
            out_list.append(modified)
    #Write data, ready for parsing, to user-specified output file
    f = open(outfile,'w')
    for line in out_list:
        f.write(line+'\n')
    f.close()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
