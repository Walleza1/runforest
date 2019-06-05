from lib.Utils import *

class CompleteNode(object):
  def __init__(self,dic={}):
    if any(dic):
      self.id = dic["id"]
      self.rate = dic["rate"]
      self.population=dic["population"]
      self.maxRate = dic["maxRate"]
      self.path = dic["path"]
      self.tDebut = dic["tDebut"]

  def load(self, node, edges):
    self.id = node.idNode
    self.population = node.pop
    self.maxRate = node.maxRate
    self.path = node.path
    self.tDebut = 0
    
    # Determiner le rate.
    # Le max rate peut faire exploser un arc. 
    # Faut choisir le min entre le min sur le chemin et le maxRate
    tmp = []
    for arc in self.path:
      tmp.append(edges[arc].capacity)
    minChemin=min(tmp)
    self.rate = min(minChemin,node.maxRate)
    return self

  def __repr__(self):
    return "{ id : "+str(self.id)+", rate : "+str(self.rate)+", maxRate : "+str(self.maxRate)+", path : "+str(self.path)+", tDebut (d'évac) : "+str(self.tDebut)+"}"
