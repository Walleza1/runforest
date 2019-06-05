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
      self.timeCalc = int(float(f.readline().strip()))
      self.metadata = f.readlines()
      self.metadata = [ x.strip() for x in self.metadata ]
      return self

  def __repr__(self):
    return "File : " + str(self.file) + "\nnodeIni: " + str(self.nodeIni) + "\nresources: "+str(self.resources).replace("]},","]},\n")+", tObjectif : "+str(self.tObjectif)+", timeCalc : "+str(self.timeCalc)+", metadata : "+str(self.metadata)+"\n"

  def verify(self):
    # Creating Blocks
    tMax=0
    #TODO
    for node in self.nodeIni:
      t = node.tDebut
      packetSize = math.ceil(node.population/node.rate)
      for ori_dest in node.path:
        resource = self.resources[ori_dest]
        # Now create block
        tEnd = t + packetSize -1
        if (node.rate > resource.capacity):
          # He is too Big for the resource
          PrintInColor.red("[ERROR] : Length exploded by nodeRate {} (max = {} nodeRate ={})".format(ori_dest,resource.capacity,node.rate))
          return False
        # Calc sum of part of resource used
        Interconnect=[c for c in resource.listBlock if not((c.tBegin < t and c.tEnd < t) or (c.tBegin > tEnd and c.tEnd > tEnd))]
        actualOccupaction=sum([c.flow for c in Interconnect])
        potentialOccupation = actualOccupaction + node.rate
        if (potentialOccupation > resource.capacity):
          PrintInColor.red("[ERROR] : Length exploded {} (max = {} actual ={})".format(ori_dest,resource.capacity,potentialOccupation))
          PrintInColor.blue("\t[DEBUG] : {}\nPotential {} (tB={}->tE={})".format(resource,node.rate,t,tEnd))
          return False
        # Everything is ok, then add this block
        resource.listBlock.append(Block(t,tEnd,node.rate,node.id))
        t = t + resource.length
        if (t > tMax):
          tMax = t
      # Vérifier que tmax respecté dans la solution
    return tMax != self.tObjectif
