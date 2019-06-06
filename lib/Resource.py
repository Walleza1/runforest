import math
from lib.Block import *
from lib.Utils import *
class Resource(object):
  def __init__(self,arc):
    self.origin = arc.origin
    self.destination = arc.destination
    self.dueDate = arc.dueDate
    self.length = arc.length
    self.capacity = arc.capacity
    self.listBlock=[]
    self.tableau={}

  def __repr__(self):
    return str(self.origin)+" -> "+str(self.destination)+" { dueDate: "+str(self.dueDate)+", length : "+str(self.length)+", capacity : "+str(self.capacity)+",listBlock : "+str(self.listBlock)+"tableau: "+str(self.tableau)+"}"
 
  def tryAddBlock(self, node, tBegin):
    # Now create block
    insertOk=False
    start = tBegin
    packetSize = math.ceil(node.population/node.rate)
    while not(insertOk):
      tEnd = start + packetSize -1
      i = start
      # Init tableau
      delta = 0
      tMax=0
      flowMax=0
      while (i <= tEnd):
        # Pas encore dedans on le crée
        if not(i in self.tableau):
          self.tableau[i]=0
        else:
          # Déjà dedans
          if (flowMax <= self.tableau[i]):
            flowMax = self.tableau[i]
            tMax = i
        i+=1
      if (flowMax + node.rate) > self.capacity:
        newTBegin = tMax+1
        deltaL= newTBegin - start
        delta += deltaL
        start = newTBegin
      else:
        return delta

  def justAddBlock(self, node, tBegin):
    packetSize = math.ceil(node.population/node.rate)
    tEnd = tBegin + packetSize-1
    i = tBegin
    while (i <= tEnd):
      self.tableau[i] += node.rate
      i+=1

  def removeTemp(self):
    for c in self.listBlock:
      if c.temp:
        self.listBlock.remove(c)

  def fixTemp(self):
    for c in self.listBlock:
      if c.temp:
        c.temp = False
