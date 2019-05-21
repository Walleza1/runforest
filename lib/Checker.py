import os, sys, copy
from lib.Probleme import *
from lib.Utils import *

class Block(object):
  def __init__(self,tBegin,tEnd,flow,temp=False):
    self.tBegin=tBegin
    self.tEnd=tEnd
    self.flow=flow
    self.temp=temp

  def __repr__(self):
    return "Block : {tBegin :"+str(self.tBegin)+",tEnd :"+str(self.tEnd)+", flow "+str(self.flow)+"}"

class CompleteNode(object):
  def __init__(self,dic={}):
    if any(dic):
      self.id = dic["id"]
      self.rate = dic["rate"]
      self.population=dic["population"]
      self.maxRate = dic["maxRate"]
      self.path = dic["path"]
      self.tDebut = dic["tDebut"]

  def load(self, node):
    self.id = node.idNode
    self.rate = node.maxRate
    self.population = node.pop
    self.maxRate = node.maxRate
    self.path = node.path
    self.tDebut = 0
    return self

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

  def addBlock(self, flow, capacity, tBegin, isLastNode, node):
    # Now create block
    tEnd = tBegin + self.length
    if (flow > self.capacity):
      # He is too Big for the ressource
      raise TypeError
    # Calc sum of part of ressource used
    actualOccupaction = sum(c.flow for c in self.listBlock if c.tBegin <= tBegin and c.tEnd >= tEnd)
    potentialOccupation = actualOccupaction + flow
    if (potentialOccupation > self.capacity):
      # Impossible to add it: shift
      newTBegin = min(c.tEnd for c in self.listBlock if c.tBegin <= tBegin and c.tEnd >= tEnd)
      delta = newTBegin - tBegin
      delta += self.addBlock(flow, capacity, newTBegin, isLastNode, node)
      return delta
    else:
      # Everything is ok, then add this block
      if (isLastNode):
        # On ajoute la durée pour évaculer tout le monde ! durée = ceil(pop/rate)
        tEnd += math.ceil(node.population / node.rate)
      self.listBlock.append(Block(tBegin, tEnd, node.rate, True))
      return 0

  def removeTemp(self):
    for c in self.listBlock:
      if c.temp:
        self.listBlock.remove(c)

  def fixTemp(self):
    for c in self.listBlock:
      if c.temp:
        c.temp = False

class Solution(object):
  def __init__(self,fichierProb="",listNoeud=[],tauxNoeud=[]):
    self.file=fichierProb
    if self.file != "":
      self.probleme = Probleme(self.file)
      self.safeNode = self.probleme.idSafeNode
      self.nodeIni = []
      for i in range(len(listNoeud)):
        self.nodeIni.append({"id": listNoeud[i], "rate": int(tauxNoeud[i]), "tDebut": 0})
      self.ressources = {}
      for arc in self.probleme.edges.items():
        # Creating id on dic
        self.ressources[arc[0]] = (Ressource(arc[1]))
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
      self.ressources = {}
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
      self.ressources = {}
      for arc in self.probleme.edges.items():
        # Creating id on dic
        self.ressources[arc[0]] = (Ressource(arc[1]))
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
    return "File : " + str(self.file) + "\nnodeIni: " + str(self.nodeIni) + "\nressources: "+str(self.ressources).replace("]},","]},\n")+", tObjectif : "+str(self.tObjectif)+", timeCalc : "+str(self.timeCalc)+", metadata : "+str(self.metadata)+"\n"

  def computeStartTime(self):
    ressourceTmp = copy.deepcopy(self.ressources)
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
