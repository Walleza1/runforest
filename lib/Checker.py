import os, sys, copy
from lib.Probleme import Edge,NodeToFree,Probleme
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

  def loadFromProbleme(self,probleme,orderNode=[],orderFlow=[],tDebut=[]):
    self.probleme = probleme
    self.safeNode = self.probleme.idSafeNode
    self.nodeIni = []
    for i in range(0,len(orderNode)):
      self.nodeIni.append({"id":int(orderNode[i]),"rate":int(orderFlow[i]),"tDebut":int(tDebut[i])})
    self.resources = {}
    for arc in self.probleme.edges.items():
      # Creating id on dic
      self.resources[arc[0]] = (Resource(arc[1]))
    tmp=[]
    for c in self.nodeIni:
      for node in self.probleme.evacuationPath:
        if node.idNode == c["id"]:
          c["population"] = node.pop
          c["maxRate"] = node.maxRate
          c["path"] = node.path
          tmp.append(CompleteNode(c))
    self.nodeIni = tmp
    self.tObjectif= int(10000)
    return self 

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
      self.tObjectif = int(f.readline().strip())
      self.timeCalc = int(float(f.readline().strip()))
      self.metadata = f.readlines()
      self.metadata = [ x.strip() for x in self.metadata ]
      return self

  def __repr__(self):
    return "File : " + str(self.file) + "\nnodeIni: " + str(self.nodeIni) + "\nresources: "+str(self.resources).replace("]},","]},\n")+", tObjectif : "+str(self.tObjectif)+", timeCalc : "+str(self.timeCalc)+", metadata : "+str(self.metadata)+"\n"

  def verify(self,verifDueDate=False):
    # Creating Blocks
    tMax=0
    tableau={}
    endsEvacuationTime=[]
    for node in self.nodeIni:
      for ori_dest in node.path:
        tableau[ori_dest] = {}
        for i in range(0,self.tObjectif+1):
          tableau[ori_dest][i] = 0
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
        # On utile un dict de ressource qui contient un dic de t.
        i = t
        if tEnd > self.tObjectif:
          PrintInColor.red("[ERROR] : tObjectif is not correct")
          return False # On dépasse la fonction objective
        while(i <= tEnd):
          tableau[ori_dest][i] += node.rate
          if tableau[ori_dest][i] > resource.capacity:
            PrintInColor.red("[ERROR] : edge {} exploded ( maxcap{} actualCap={}) at t= {}".format(ori_dest,resource.capacity,tableau[ori_dest][i],i))
            return False
          if verifDueDate:
            if (i > resource.dueDate):
              PrintInColor.red("[ERROR] : arc {} dueDate {} at {}".format(ori_dest,resource.dueDate,i))
              return False
          i+=1
        t = t + resource.length
        if ori_dest[1] == self.safeNode:
          endsEvacuationTime.append(t+packetSize)
      # Vérifier que tmax respecté dans la solution
#      tMax += packetSize -1
    tMax=max(endsEvacuationTime)
    return tMax == self.tObjectif

  def getFindEvac(self):
    # Creating Blocks
    tMax=0
    endsEvacuationTime=[]
    tableau={}
    for node in self.nodeIni:
      for ori_dest in node.path:
        tableau[ori_dest] = {}
    for node in self.nodeIni:
      t = node.tDebut
      packetSize = math.ceil(node.population/node.rate)
      for ori_dest in node.path:
        resource = self.resources[ori_dest]
        # Now create block
        tEnd = t + packetSize-1
        # On utile un dict de ressource qui contient un dic de t.
        i = t
        while(i <= tEnd):
          if not(i in tableau[ori_dest]):
            tableau[ori_dest][i] = 0
          tableau[ori_dest][i] += node.rate
          i+=1
        t = t + resource.length
        if ori_dest[1] == self.safeNode:
          endsEvacuationTime.append(t+packetSize)
      # Vérifier que tmax respecté dans la solution
    tMax=max(endsEvacuationTime)
    return tMax 

  def isCapValid(self,debug=True):
    # Creating Blocks
    tableau={}
    for node in self.nodeIni:
      for ori_dest in node.path:
        tableau[ori_dest] = {}
    for node in self.nodeIni:
      t = node.tDebut
      packetSize = math.ceil(node.population/node.rate)
      for ori_dest in node.path:
        resource = self.resources[ori_dest]
        # Now create block
        tEnd = t + packetSize -1
        if (node.rate > resource.capacity):
          # He is too Big for the resource
          if debug:
            PrintInColor.red("[ERROR] : Length exploded by nodeRate {} (max = {} nodeRate ={})".format(ori_dest,resource.capacity,node.rate))
          return False
        i = t
        while(i <= tEnd):
          if not(i in tableau[ori_dest]):
            tableau[ori_dest][i] = 0
          tableau[ori_dest][i] += node.rate
          if tableau[ori_dest][i] > resource.capacity:
            if debug:
              PrintInColor.red("[ERROR] : edge {} exploded ( maxcap{} actualCap={}) at t= {}".format(ori_dest,resource.capacity,tableau[ori_dest][i],i))
              PrintInColor.red(tableau[ori_dest])
            return False
          i+=1
        t = t + resource.length
      # Vérifier que tmax respecté dans la solution
    return True

  def writeSolution(self,filename):
    with open(filename,'w') as f:
      instance_name=self.probleme.source_file.replace("Instances/","").replace(".full","")
      f.write(instance_name+ "\n")
      f.write("{}\n".format(self.probleme.N))
      for node in self.nodeIni:
        f.write("{} {} {}\n".format(node.id,node.rate,node.tDebut))
      self.tObjectif = self.getFindEvac()
      f.write("valid\n")
      f.write("{}\n".format(self.tObjectif))
      f.write("{}\n".format(0))
      f.write("After compact data from max")
      
