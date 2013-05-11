#!/usr/bin/python
import sys

def main(args):
	if len(args) < 2:
		print "Usage: python eval_ls.py data_to_eval"
		return 1
	gold = [int(item.strip()) for item in open('developmentSetLabels.dat').readlines()]
	ours = [int(item.strip().split()[-1]) for item in open(args[1]).readlines()]
	acc = 0.0
	assert len(gold) == len(ours)
	for i in xrange(len(gold)):
		if gold[i] == ours[i]:
			acc += 1.
	print str(int(acc))+" labels correct out of "+str(int(len(gold)))
	print str(acc/200)+" accuracy"
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
