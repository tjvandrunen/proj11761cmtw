#!/usr/bin/python
#lns_tag_format.py
#Weston Feely
#4/17/13
import sys

#Formats parsed data into a easily-readable tagged data file
#Also adds document boundaries back into parsed data file
def main(args):
    #Check for required args
    if len(args) < 4:
        print "Usage: python lns_tag_format.py input_filename input_filename.parsed output_filename"
        return 1
    #Read in args
    corpus = open(args[1]).readlines()
    parsed_corpus = open(args[2]).readlines()
    output_fn = args[3]
    #Make a copy of the input corpus, save as output list
    out_list = list(corpus)
    #Loop through parsed corpus
    buff = ["<s>"] # sentence list buffer
    i=0 # index for current out_list sentence
    for line in parsed_corpus:
        if line.isspace():
            #End of parsed sentence
            buff.append("</s>\n")
            #Check to see if current output list sentence is a document boundary
            if set(list(out_list[i].strip())) == set(['~']):
                i+=1 # increment sentence number
            #Replace output list sentence with joined buffer
            out_list[i] = ' '.join(buff)
            #Restart buffer
            buff = ["<s>"]
            i+=1 # increment sentence number
        else:
            #Append next token+tag pair to buffer
            lis = line.split('\t')
            token = lis[1]
            tag = lis[3]
            buff.append(token+'/'+tag)
    #Add context cues back into parsed data file
    sent_list = [] # list of lists; compresses multi-line parsed sentences back into single entries in this list
    buff = [] # sentence list buffer
    for line in parsed_corpus:
        if line.isspace():
            #Append latest sentence (a list) to sent_list
            sent_list.append(buff)
            buff = [] # clear buffer
        else:
            buff.append(line) # append line to buffer
    #Make a copy of the original corpus
    parsed_corpus_fixed = list(corpus)
    #Replace each non-sentence-boundary string in parsed_corpus_fixed with the next sentence (a list) from sent_list
    i=0
    for lis in sent_list:
        #Check to see if current parsed_corpus_fixed sentence is a document boundary
        if set(list(parsed_corpus_fixed[i].strip())) == set(['~']):
            i+=1 # increment sentence number
        #Replace sentence in parsed_corpus_fixed with sentence (a list) from sent_list
        parsed_corpus_fixed[i] = lis
        i+=1 # increment sentence number
    #Write output list to output file
    f = open(output_fn,'w')
    for line in out_list:
        f.write(line)
    f.close()
    #Write parsed data file with added document boundary markers
    f = open(args[2]+'.fixed','w')
    for item in parsed_corpus_fixed:
        if item is str:
            #Write document boundary marker to file
            f.write(item)
        else:
            #Write each line in this parsed sentence (a list) to file
            for line in item:
                f.write(line)
    f.close()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
