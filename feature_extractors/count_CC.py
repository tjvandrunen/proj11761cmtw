#!/usr/bin/python
#Callie Vaughn and Wes Feely
#CMU 2013
import sys

#Extracts a feature for number of consecutive CCs in each document, normalized by the number of words in the document
def main(args):
	if len(args) < 2:
		print "Usage: python count_CC.py tag_stream_file"
		return 1
	tag_fname = args[1]
	f = open(tag_fname, 'r')
	i = 1 # document counter
	j = 0 # word counter (per document)
	count = 0 # count of CCs in each document
	for line in f:
		#Check for document boundary marker (except the first one)
		if set(list(line.strip())) == set(['~']) and j!=0:
			#Print count/#words in doc for this document
			print count*1.0/j
			count = 0
			i += 1
			j = 0
		else:
			#Check for repeated CCs
			ls = line.strip().split()
			last = ''
			for wd in ls:
				j += 1
				curr = wd
				#Increment count if we've found a consecutive CC pair
				if curr==last=='CC':
					count += 1
				last = curr
	#Print counts for final document
	if j!=0:
		print count*1.0/j
	return 0

if __name__ == "__main__":
	sys.exit(main(sys.argv))
