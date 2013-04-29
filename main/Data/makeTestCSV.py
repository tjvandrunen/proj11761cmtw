import csv, sys, re

testData = sys.argv[1]
outFile = open(sys.argv[2],'w')
writer = csv.writer(outFile)
doc = []
index = 0
for line in open(testData):
  if line[0]=='~':
    if len(doc)>0:
      index += 1
      writer.writerow([str(index),' '.join(map(lambda x:re.match(r"<s>(.*)</s>",x).group(1).lower(), doc))])
      doc = []
  else:
    doc.append(line.strip())
if len(doc)>0:
  writer.writerow([str(index+1),' '.join(map(lambda x:re.match(r"<s>(.*)</s>",x).group(1).lower(), doc))])
outFile.close()
