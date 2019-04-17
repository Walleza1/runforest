#!/usr/bin/env python3

import os, sys
from Probleme import Probleme

class Solution:
  def __init__(self,source_file):
    header=True
    headerSize=0
    with open(source_file) as f:
      # Verifier que le fichier existe
      self.file='Instances/'+f.readline().replace("\n","")+".full"
      if not(os.path.isfile(self.file)):
        print("Error file unknown")
        exit(1)
      self.probleme=Probleme(self.file)
      headerSize=int(f.readline())
      self.nodeIni=[]
      for i in range(headerSize):
        temp=f.readline().split()
        self.nodeIni.append({"node":int(temp[0]),"rate":int(temp[1]),"t":int(temp[2])})
        i+=1
      self.isValid=True if f.readline().strip().lower() == "valid" else False
      self.fObjectif=f.readline()
      self.timeCalc=float(f.readline())
      self.metadata=f.readlines()
      self.metadata=[x.strip() for x in self.metadata]

  def solve(self):
    t=0
    # Technique dictionnaire 
    # clef t
    # contenant un dic contenant 2 dic (arc) & (node)
    # clef(arc) = (v1,v2)
    # clef(node) = (v1)
    etat={t:{'arc':{},'node':{}}} 
    print(self.probleme)
    for arc in self.probleme.edges.items():
      etat[t]['arc'][arc[0]]=arc
      etat[t]['arc'][arc[0]][1]['flow']=0
    return etat

  def __repr__(self):
    return "File : "+str(self.file)+"\nProbleme : "+str(self.probleme)+"\n"


def main():
  obj=Solution("solution")
  print(obj.solve())

if __name__ == "__main__":
  main()
