import sys
import math
from graphviz import Digraph

class Edge(object):
  def __init__(self,origin,destination,dueDate,length,capacity):
    self.origin = origin
    self.destination = destination
    self.dueDate = dueDate
    self.length = length
    self.capacity = capacity

  def __repr__(self):
    return str(self.origin)+" -> "+str(self.destination)+" [ dueDate: "+str(self.dueDate)+", length : "+str(self.length)+", capacity : "+str(self.capacity);

class NodeToFree(object):
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
    self.nodes=[idNode]+path
    self.path = self.rebuildpath([idNode] + path)

  def __repr__(self):
    return "idNode : "+str(self.idNode)+"\npopulation : "+str(self.pop)+"\nMaxRate : "+str(self.maxRate)+"\ndistanceToSafe : "+str(self.distanceToSafe)+"\nPath: : "+str(self.path)+"\n\n"


class Probleme(object):
  def __init__(self, source_file):
    self.source_file = source_file;
    with open(source_file) as f:
      # Readline starts with c
      line = f.readline()
      # Read header
      line = f.readline().split()
      self.N = int(line[0])
      self.idSafeNode = int(line[1])
      evacuationPathTemp = []
      self.edges=dict()
      # Parcours de NodeToFree 
      for i in range(0,self.N):
        temp = [ int(x) for x in f.readline().split() ]
        evacuationPathTemp.append(NodeToFree(temp.pop(0),temp.pop(0),temp.pop(0),temp.pop(0),temp))
      self.evacuationPath=evacuationPathTemp
      # Merge Edges
      edges = [ x.path for x in evacuationPathTemp ]
      listOfEdges = []
      for x in edges:
        listOfEdges += x
      listOfEdges = list(set(listOfEdges))
      # Header (c) for Graph
      line = f.readline()
      # Header for Graph
      line = f.readline().split()
      arcNb = int(line[1])
      for i in range(0,arcNb):
        line = [ int(x) for x in f.readline().split() ]
        origin = line[0]
        dest = line[1]
        dueDate=line[2]
        length=line[3]
        capacity=line[4]
        if ( (origin,dest) in listOfEdges ):
          self.edges[ (origin,dest) ]=Edge(origin,dest,dueDate,length,capacity)
        if ( (dest,origin) in listOfEdges ):
          self.edges[ (dest,origin) ]=Edge(dest,origin,dueDate,length,capacity)

  def renderPath(self,output="output"): 
    dot = Digraph('G',filename=output,format='png') 
    dot.attr('graph',concentrate='true')
    dot.node(str(self.idSafeNode),shape='doublecircle')
    for edge in self.edges:
        dot.edge(str(edge[0]),str(edge[1]))
    dot.view()

  def __repr__(self):
    return "Problème : "+self.source_file+"\nevacuationPath : "+str(self.evacuationPath)+"\nedges : "+str(self.edges)
