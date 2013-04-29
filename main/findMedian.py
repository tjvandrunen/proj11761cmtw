#!/usr/bin/python

import sys

def main(args):

	f = open(args[1], 'r')
	o = open(args[2], 'w+')

	for line in f:
		ls = line.strip().split(',')
		if len(ls)<3:
			print "ERROR ERROR ERROR ERROR ERROR"
			return 1
		else:
			ls = ls[1:]
			vals=[]
			for feat in ls:
				val = float(feat)
				vals.append(val)
			vals.sort()
			middle = len(vals)/2.0
			if int(middle) == middle:
				mid1 = vals[int(middle-1)]
				mid2 = vals[int(middle)]
				ls.append("%f" % ((mid1+mid2)/2.0))
			else:
				ls.append("%f" % (vals[int(middle)]))
			o.write("%s\n" % ','.join(ls))
			
	return 0

if __name__ == "__main__":
	sys.exit(main(sys.argv))
