import math
from lib.Block import *

class Resource(object):
  def __init__(self,arc):
    self.origin = arc.origin
    self.destination = arc.destination
    self.dueDate = arc.dueDate
    self.length = arc.length
    self.capacity = arc.capacity
    self.listBlock=[]

  def __repr__(self):
    return str(self.origin)+" -> "+str(self.destination)+" { dueDate: "+str(self.dueDate)+", length : "+str(self.length)+", capacity : "+str(self.capacity)+",listBlock : "+str(self.listBlock)+"}"

  def addBlock(self, tBegin, isLastNode, node):
    flow = node.rate
    # Now create block
    tEnd = tBegin + self.length
    if flow > self.capacity:
      # He is too Big for the ressource
      raise Exception("Overflow")
    # Calc sum of part of ressource used
    actualOccupaction = sum(c.flow for c in self.listBlock if c.tBegin <= tBegin and c.tEnd >= tEnd)
    potentialOccupation = actualOccupaction + flow
    if potentialOccupation > self.capacity:
      # Impossible to add it: shift
      newTBegin = min(c.tEnd for c in self.listBlock if c.tBegin <= tBegin and c.tEnd >= tEnd)
      delta = newTBegin - tBegin
      delta += self.addBlock(newTBegin, isLastNode, node)
      return delta
    else:
      # Everything is ok, then add this block
      if isLastNode:
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