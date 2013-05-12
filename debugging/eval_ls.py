#!/usr/bin/python
import sys

def main(args):
	if len(args) < 2:
		print "Usage: python eval_ls.py labels_to_eval gold_labels"
		return 1
	ours = [int(item.strip().split()[-1]) for item in open(args[1]).readlines()]
	gold = [int(item.strip()) for item in open(args[2]).readlines()]	
	acc = 0.0
	assert len(gold) == len(ours)
	for i in xrange(len(gold)):
		if gold[i] == ours[i]:
			acc += 1.
	print str(int(acc))+" labels correct out of "+str(int(len(gold)))
	print str(acc/int(len(gold)))+" accuracy"
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
