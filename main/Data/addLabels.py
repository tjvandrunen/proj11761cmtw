import csv, sys


header = ["election","y2k","russia-nafta","stock-market","health-care","blah","school-violence","clinton","bosnia","civil-rights","junk","budget","medicine","entertainment","family","court","junk2","transitions","military","media","Median"]
topicsFile = sys.argv[1]
labels = [line.strip() for line in open(sys.argv[2])]
text = [line[1] for line in csv.reader(open(sys.argv[3]))]
outFile = open(sys.argv[4],'w')
outFile.write("Document,"+','.join(header)+",Label,Text\n")
writer = csv.writer(outFile)
index = 0
for line in open(topicsFile):
  writer.writerow(line.strip().split(",")+[labels[index]]+[text[index]])
  index += 1
outFile.close()
