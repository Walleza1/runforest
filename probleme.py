#!/usr/bin/env python3

import sys
import math

class NodeToFree():
  def rebuildpath(self,path):
    res=[]
    for i in path:
      if path.index(i)+1 < len(path):
        res.append((i,path[path.index(i)+1]))
    return res

  def __init__(self,idNode,pop,maxRate,distanceToSafe,path):
    self.idNode=idNode
    self.pop=pop
    self.maxRate=maxRate
    self.distanceToSafe=distanceToSafe 
    self.path = self.rebuildpath([idNode] + path)

  def __repr__(self):
    return "idNode : "+str(self.idNode)+"\npopulation : "+str(self.pop)+"\nMaxRate : "+str(self.maxRate)+"\ndistanceToSafe : "+str(self.distanceToSafe)+"\nPath: : "+str(self.path)+"\n\n"


class Probleme:

  def __init__(self,source_file):
    self.source_file=source_file
    headerPath = True
    readerPath = False
    nbPath=0
    idSafeNode=0
    i=0
    headerGraph = True
    readerGraph = False
    self.Graph={}
    listOfEdges=[]
    graphNode=0
    graphEdge=0
    self.evacuationPath=[]
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
              self.evacuationPath.append(NodeToFree(temp.pop(0),temp.pop(0),temp.pop(0),temp.pop(0),temp))
              i += 1
            else:
              readerPath=False
          if (not(readerPath)):
            if (headerGraph):
              for path in self.evacuationPath:
                listOfEdges += path.path
              listOfEdges=list(set(listOfEdges))
              listOfEdges.sort()
              graphNode=int(line.split()[0])
              graphEdge=int(line.split()[1])
              i=0
              headerGraph=False
              readerGraph=True
              continue
            if (readerGraph):
              if (i < graphEdge):
                temp=line.split()
                origin=int(temp[0])
                dest=int(temp[1])
                if ( (origin,dest) in listOfEdges or (dest,origin) in listOfEdges):
                  distance=int(math.ceil(float(temp[3])))
                  capacite=int(math.floor(float(temp[4])))
                  self.Graph[(origin,dest)]={"distance": distance, "dueDate":int(temp[2]),"capacite":capacite}


  def __repr__(self):
    return "Problème : "+self.source_file+"\nevacuationPath : "+str(self.evacuationPath)+"\nGraph : "+str(self.Graph)+"\n\n"

def main(source_file):
  obj=Probleme(source_file) 
  print(obj)

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Give a path to a file to read")
    exit(1)
  main(sys.argv[1])
