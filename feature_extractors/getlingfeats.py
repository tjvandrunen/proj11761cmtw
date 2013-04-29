#!/usr/bin/python
#getlingfeats.py
#Wes Feely, Mario Piergallini, Tom van Drunen, Callie Vaughn
#CMU 2013
#4/28/13
import sys, re
from collections import Counter

#Extracts linguistic features for each document in input files (file1=tag file, file2=parse file)
#Returns one feature vector per line, space-separated
#Features:
# document length (in words)
# number of DEP labels in parses for document
# number of consecutive CC, DT, POS in tags for document
# number of repeated words in document
def main(args):
	#Check for required args
	if len(args) < 3:
		print "Usage: python getlingfeats.py tag_file parse_file"
		return 1
	#Read in files
	tag_file_raw = open(args[1]).readlines()
	parse_file_raw = open(args[2]).readlines()
	judg = open("../data/original_data/developmentSetLabels.dat").readlines()
	judg = [x.strip() for x in judg]
	#Organize files into a list of docs (where each doc is a long string)
	tag_docs = []
	parse_docs = []
	buff = []
	for line in tag_file_raw[1:]:
		if set(list(line.strip())) == set(['~']):
			tag_docs.append(' '.join(buff))
			buff = []
		else:
			buff.append(line.strip())
	tag_docs.append(' '.join(buff))
	buff = []
	for line in parse_file_raw[1:]:
		if set(list(line.strip())) == set(['~']):
			parse_docs.append(' '.join(buff))
			buff = []
		else:
			buff.append(line.strip())
	parse_docs.append(' '.join(buff))
	#Verify number of docs
	assert len(tag_docs) == len(parse_docs)	
	#Extract features
	bad_tags = ['DT','CC','POS']
	feats = []
	for i in xrange(0,len(tag_docs)):
		tagdoc = tag_docs[i]
		tagstream = []
		wordstream = []
		for item in tagdoc.strip().split():
			if not (item == "<s>" or item == "</s>"):
				tagstream.append(item.split('/')[1])
				wordstream.append(item.split('/')[0])
		parsedoc = parse_docs[i]
		vec = [] # feature vector for this document
		#Add length of document to vector
		vec.append(len(tagdoc.strip().split()))
		#Add number of DEP labels to vector
		vec.append(len([x for x in parsedoc.split() if x=="DEP"]))
		#Add number of consecutive bad tags to vector
		num_consec_badtags = 0
		for badtag in bad_tags:
			prev_tag = ''
			for tag in tagstream:
				if prev_tag == tag == badtag:
					num_consec_badtags += 1
				prev_tag = tag
		vec.append(num_consec_badtags)
		#Add number of repeated words to vector
		num_repeat = 0
		doc_counter = Counter(wordstream)
		vec.append(sum([doc_counter[x] for x in doc_counter if doc_counter[x] > 1]))
		#Normalize features and convert each feature to string
		vec_str = []
		vec_str.append(str(vec[0]))
		for j in xrange(1,len(vec)):
			feat = float(vec[j]) / vec[0]
			vec_str.append(str(feat))
		#Print features to stdout
		print judg[i]+' '+' '.join(vec_str)
		#print ' '.join(vec_str)
	return 0

if __name__ == "__main__":
	sys.exit(main(sys.argv))
