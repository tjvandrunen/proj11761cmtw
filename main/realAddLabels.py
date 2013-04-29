#!/usr/bin/python

import sys

def main(args):
    f = open(args[1], 'r')
    lf = open(args[2], 'r')
    feats = open(args[3], 'r')
    o = open(args[4], 'w+')
    
    feat_list = []

    for line in feats:
        ls = line.strip().split(' ')
        num_feats = len(ls)
        feat_list.append(ls)
        

    o.write("class T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 T13 T14 T15 T16 T17 T18 T19 T20 median")
    for x in range(num_feats):
        o.write(" f%d" % x)
    o.write('\n')

    labels = []
    for line in lf:
        if line.strip()=='0':
            labels.append('FALSE')
        elif line.strip()=='1':
            labels.append('TRUE')
        else:
            print "ERROR"
#        labels.append(line.strip())

    i=0
    for line in f:
        fin = []
        fin.append(labels[i])
        
        ls = line.strip().split(',')
        fin = fin + ls + feat_list[i]

        st = ' '.join(fin)
#        st = ' '.join([str(x) for x in fin])
        o.write("%s\n" % st)
        i+=1


if __name__=="__main__":
    sys.exit(main(sys.argv))
