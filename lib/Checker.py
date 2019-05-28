import os, sys, copy
from lib.Probleme import *
from lib.Utils import *
from lib.CompleteNode import *
from lib.Resource import *
from lib.Block import *

class Solution(object):
  def __init__(self,fichierProb="",listNoeud=[],tauxNoeud=[]):
    self.file=fichierProb
    if self.file != "":
      self.probleme = Probleme(self.file)
      self.safeNode = self.probleme.idSafeNode
      self.nodeIni = []
      for i in range(len(listNoeud)):
        self.nodeIni.append({"id": listNoeud[i], "rate": int(tauxNoeud[i]), "tDebut": 0})
      self.resources = {}
      for arc in self.probleme.edges.items():
        # Creating id on dic
        self.resources[arc[0]] = (Resource(arc[1]))
      tmp=[]
      for c in self.nodeIni:
        for node in self.probleme.evacuationPath:
          if node.idNode == c["id"]:
            c["population"]=node.pop
            c["maxRate"]=node.maxRate
            c["path"]=node.path
            tmp.append(CompleteNode(c))
      self.nodeIni = tmp
    else:
      self.probleme = None
      self.safeNode = None
      self.nodeIni = []
      self.resources = {}
    self.tObjectif = math.inf
    self.metadata = []
    self.timeCalc = 0

  def load(self,source_file):
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
      self.resources = {}
      for arc in self.probleme.edges.items():
        # Creating id on dic
        self.resources[arc[0]] = (Resource(arc[1]))
      self.isValid = True if f.readline().strip().lower() == "valid" else False
      tmp=[]
      for c in self.nodeIni:
        for node in self.probleme.evacuationPath:
          if node.idNode == c["id"]:
            c["population"] = node.pop
            c["maxRate"] = node.maxRate
            c["path"] = node.path
            tmp.append(CompleteNode(c))
      self.nodeIni = tmp
      self.tObjectif = f.readline()
      self.timeCalc = int(f.readline())
      self.metadata = f.readlines()
      self.metadata = [ x.strip() for x in self.metadata ]
      return self

  def __repr__(self):
    return "File : " + str(self.file) + "\nnodeIni: " + str(self.nodeIni) + "\nresources: "+str(self.resources).replace("]},","]},\n")+", tObjectif : "+str(self.tObjectif)+", timeCalc : "+str(self.timeCalc)+", metadata : "+str(self.metadata)+"\n"

  def computeStartTime(self):
    resourceTmp = copy.deepcopy(self.resources)
    for node in self.nodeIni:
      print(node)
      for arc in node.path:
        print(arc)

  def verify(self):
    # Creating Blocks
    tMax=0
    for node in self.nodeIni:
      t=node.tDebut
      for ori_dest in node.path:
        resource = self.resources[ori_dest]
        # Now create block
        tEnd=t+resource.length
        if (node.rate > resource.capacity):
          # He is too Big for the resource
          return False
        # Calc sum of part of resource used
        actualOccupaction=sum(c.flow for c in resource.listBlock if c.tBegin <= t and c.tEnd >= tEnd)
        potentialOccupation=actualOccupaction + node.rate
        if (potentialOccupation > resource.capacity):
          return False
        # Everything is ok, then add this block
        if (ori_dest[1] == self.safeNode):
          # On ajoute la durée pour évaculer tout le monde ! durée = ceil(pop/rate)
          tEnd += math.ceil(node.population/node.rate)
        resource.listBlock.append(Block(t,tEnd,node.rate))
        t=tEnd
        if (t > tMax):
          tMax = t
      print(self)

      # Vérifier que tmax respecté dans la solution
    return tMax != self.tObjectif
