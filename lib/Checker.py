import os, sys
from lib.Probleme import *
from lib.Utils import *

class Block(object):
  def __init__(self,tBegin,tEnd,flow):
    self.tBegin=tBegin
    self.tEnd=tEnd
    self.flow=flow

  def __repr__(self):
    return "Block : {tBegin :"+str(self.tBegin)+",tEnd :"+str(self.tEnd)+", flow "+str(self.flow)+"}"

class CompleteNode(object):
  def __init__(self,dic):
    self.id = dic["id"]
    self.rate = dic["rate"]
    self.population=dic["population"]
    self.maxRate = dic["maxRate"]
    self.path = dic["path"]
    self.tDebut = dic["tDebut"]

  def __repr__(self):
    return "{ id : "+str(self.id)+", rate : "+str(self.rate)+", maxRate : "+str(self.maxRate)+", path : "+str(self.path)+", tDebut (d'évac) : "+str(self.tDebut)+"\n"

class Ressource(object):
  def __init__(self,arc):
    self.origin = arc.origin
    self.destination = arc.destination
    self.dueDate = arc.dueDate
    self.length = arc.length
    self.capacity = arc.capacity
    self.listBlock=[]

  def __repr__(self):
    return str(self.origin)+" -> "+str(self.destination)+" { dueDate: "+str(self.dueDate)+", length : "+str(self.length)+", capacity : "+str(self.capacity)+",listBlock : "+str(self.listBlock)+"}"

class Solution(object):
  def __init__(self,source_file):
    header = True
    headerSize = 0
    with open(source_file) as f:
      # Verifier que le fichier existe
      self.file = 'Instances/' + f.readline().replace("\n","") + ".full"
      if not(os.path.isfile(self.file)):
        print("Error file unknown")
        exit(1)
      self.probleme = Probleme(self.file)
      headerSize = int(f.readline())
      self.safeNode= self.probleme.idSafeNode
      self.nodeIni = []
      for i in range(headerSize):
        temp = f.readline().split()
        self.nodeIni.append({"id":int(temp[0]),"rate":int(temp[1]),"tDebut":int(temp[2])})
        i+=1
      self.ressources = {}
      for arc in self.probleme.edges.items():
        # Creating id on dic
        self.ressources[arc[0]] = (Ressource(arc[1]))
      self.isValid = True if f.readline().strip().lower() == "valid" else False
      tmp=[]
      for node in self.probleme.evacuationPath:
        for c in self.nodeIni:
          if node.idNode == c["id"]:
            c["population"]=node.pop
            c["maxRate"]=node.maxRate
            c["path"]=node.path
            tmp.append(CompleteNode(c))
      self.nodeIni = tmp
      self.tObjectif = f.readline()
      self.timeCalc = int(f.readline())
      self.metadata = f.readlines()
      self.metadata = [ x.strip() for x in self.metadata ]

  def __repr__(self):
    return "File : " + str(self.file) + "\nnodeIni: " + str(self.nodeIni) + "\nressources: "+str(self.ressources).replace("]},","]},\n")+", tObjectif : "+str(self.tObjectif)+", timeCalc : "+str(self.timeCalc)+", metadata : "+str(self.metadata)+"\n"

  def verify(self):
    # Creating Blocks
    tMax=0
    for node in self.nodeIni:
      t=node.tDebut
      for ori_dest in node.path:
        ressource = self.ressources[ori_dest]
        # Now create block
        tEnd=t+ressource.length
        if (node.rate > ressource.capacity):
          # He is too Big for the ressource
          return False
        # Calc sum of part of ressource used
        actualOccupaction=sum(c.flow for c in ressource.listBlock if c.tBegin <= t and c.tEnd >= tEnd)
        potentialOccupation=actualOccupaction + node.rate
        if (potentialOccupation > ressource.capacity):
          return False
        # Everything is ok, then add this block
        if (ori_dest[1] == self.safeNode):
          # On ajoute la durée pour évaculer tout le monde ! durée = ceil(pop/rate)
          tEnd += math.ceil(node.population/node.rate)
        ressource.listBlock.append(Block(t,tEnd,node.rate))
        t=tEnd
        if (t > tMax):
          tMax = t
      print(self)

      # Vérifier que tmax respecté dans la solution
    return tMax != self.tObjectif
