#!/usr/bin/env python3

import sys

class NodeToFree():

  def __init__(self,idNode,pop,maxRate,distanceToSafe,path):
    self.idNode=idNode
    self.pop=pop
    self.maxRate=maxRate
    self.distanceToSafe=distanceToSafe
    self.path=path

  def __repr__(self):
    return "idNode : "+str(self.idNode)+"\npopulation : "+str(self.pop)+"\nMaxRate : "+str(self.maxRate)+"\ndistanceToSafe : "+str(self.distanceToSafe)+"\nPath: : "+str(self.path)+"\n"


def readFile(source_file):
  headerPath = True
  readerPath = False
  nbPath=0
  idSafeNode=0
  i=0
  evacuationPath=[]
  with open(source_file) as f:
    content = f.readlines()
    for line in content:
      if not(line.startswith("c")):
       # print(line.replace("\n",""))
        if headerPath:
          nbPath=int(line.split()[0])
          idSafeNode=int(line.split()[1])
          headerPath=False
          readerPath=True
          continue
        if readerPath:
          if (i < nbPath):
            temp=list(map(int,line.split()))
            evacuationPath.append(NodeToFree(temp.pop(0),temp.pop(0),temp.pop(0),temp.pop(0),temp))
            i += 1
          else:
            readerPath=False
  print(evacuationPath)



def main(source_file):
  obj=readFile(source_file) 


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Give a path to a file to read")
    exit(1)
  main(sys.argv[1])
