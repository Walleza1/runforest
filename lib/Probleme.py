import copy
import sys
import math
import time
from graphviz import Digraph

from lib.CompleteNode import *
from lib.Resource import *
from lib.Utils import *
#from lib.Checker import *

class Edge(object):
  def __init__(self,origin,destination,dueDate,length,capacity):
    self.origin = origin
    self.destination = destination
    self.dueDate = dueDate
    self.length = length
    self.capacity = capacity

  def __repr__(self):
    return str(self.origin)+" -> "+str(self.destination)+" [ dueDate: "+str(self.dueDate)+", length : "+str(self.length)+", capacity : "+str(self.capacity)

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

def printDebug(msg, debug):
  if debug:
    PrintInColor.blue(msg, end='', flush=False)

class Probleme(object):
  def __init__(self, source_file):
    self.source_file = source_file
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

  def minimum(self, output, debug):
    min_value = 0

    file = open(output, "w")
    file.write(output + "\n")
    file.write(str(self.N) + "\n")

    timestamp = time.time()

    printDebug("\n\n##########\n" + self.__repr__() + "\n##########\n\n", debug)

    printDebug("Probleme::minimum: Beginning, min = " + str(min_value) + "\n", debug)

    for node in self.evacuationPath:
      value = 0
      for edge in node.path:
        value += self.edges[edge].length
      file.write(str(node.idNode) + ", " + str(value) + ", " + str(0) + "\n")

      printDebug("Probleme::minimum: path length from node " + str(node.idNode) + ": " + str(value) + "+" + str(math.ceil(node.pop / node.maxRate)), debug)
      value += math.ceil(node.pop / node.maxRate)

      if value > min_value:
        min_value = value
        printDebug(", which is the best value", debug)
      printDebug("\n", debug)

    execution_time = time.time() - timestamp

    file.write("invalid\n")
    file.write(str(min_value) + "\n")
    file.write(str(execution_time) + "\n")
    file.write("handmade 0.1.0\n")
    file.write("\"everyone evacuates from start ; no constraint check\"\n")
    file.close()

    return min_value

  def maximum(self, output, debug):
    # TODO : nouvelle manière de faire
    # 1. Choisir un ordre de séquencement
    #  -> ordre décroissant de la distance (chemin critique d'abord)
    #  -> ordre croissant du temps de parcours (nodes à côté de la sortie, faciles à faire partir)
    # 2. Placer les points
    #  -> stratégie au plus tôt : placement du 1er node de la séquence puis les autres pour que ça marche
    #  -> choix du taux maximum sur tout le chemin
    #  -> choix du taux maximisé par noeud
    # 3. Trouver un voisinnage local
    #  -> intervertir des ressources localement et donner du mou, de manière exhaustive ?
    # 4. Compacter
    #  -> boucler sur chaque noeud et essayer de le pousser vers la gauche ; continuer jusqu'à ce que ça soit impossible
    max_value = 0

    file = open(output, "w")
    file.write(output + "\n")
    file.write(str(self.N) + "\n")

    timestamp = time.time()

    printDebug("\n\n##########\n" + self.__repr__() + "\n##########\n\n", debug)

    printDebug("Probleme::maximum: Beginning, max = " + str(max_value) + "\n", debug)

    for node in self.evacuationPath:
      for edge in node.path:
        max_value += self.edges[edge].length
      file.write(str(node.idNode) + ", " + str(max_value) + ", " + str(0) + "\n")

      printDebug("Probleme::maximum: total path length at node " + str(node.idNode) + ": " + str(max_value) + "+" + str(math.ceil(node.pop / node.maxRate)) + "\n", debug)
      max_value += math.ceil(node.pop / node.maxRate)

    execution_time = time.time() - timestamp

    file.write("invalid\n")
    file.write(str(max_value) + "\n")
    file.write(str(execution_time) + "\n")
    file.write("handmade 0.1.0\n")
    file.write("\"everyone evacuates from start ; no constraint check\"\n")
    file.close()

    return max_value

  def sequence_ordering(self, debug):
    # Sequence ordering: calculation of all distances for each node
    lengths = {}
    for node in self.evacuationPath:
      my_node = CompleteNode().load(node)
      lengths[my_node] = math.ceil(my_node.population / my_node.rate)
      for edge in node.path:
        lengths[my_node] += self.edges[edge].length

    # Total duration sorted by 'max duration first'
    lengths_ordered = sorted(lengths.items(), key=lambda kv: kv[1], reverse=True)
    sequence = []
    for node in lengths_ordered:
      sequence.append(node)
      printDebug(str(node[0].id) + " (" + str(lengths[node[0]]) + ")\n", debug)
    return sequence

  def resources_placement(self, sequence_order):
    resources = {}

    for node in sequence_order:
      isDoneOnce = False
      delta = 0
      wasDeltaIncremented = False
      while not isDoneOnce or wasDeltaIncremented:
        tTotal = math.ceil(node[0].population / node[0].rate)
        for edge in node[0].path:
          tTotal += self.edges[edge].length

        isDoneOnce = True
        isLastNode = True

        p_reversed = copy.deepcopy(node[0].path)
        p_reversed.reverse()
        for edge in p_reversed:
          # The resource already exists
          tTotal -= self.edges[edge].length
          if not edge[0] in resources:
            resources[edge[0]] = Resource(self.edges[edge])
          resources[edge[0]].removeTemp()
          newDelta = resources[edge[0]].addBlock(tTotal + delta, isLastNode, node[0])
          if newDelta != 0:
            wasDeltaIncremented = True
            delta += newDelta
          isLastNode = False
      for res in resources.items():
        res[1].fixTemp()

  def compute_solution(self, output, debug):
    max_value = 0

    file = open(output, "w")
    file.write(output + "\n")
    file.write(str(self.N) + "\n")

    timestamp = time.time()

    printDebug("\n\n##########\n" + self.__repr__() + "\n##########\n\n", debug)
    printDebug("Probleme::maximum: Beginning, max = " + str(max_value) + "\n", debug)

    sequence_order = self.sequence_ordering(debug)
    self.resources_placement(sequence_order)


  def __repr__(self):
    return "Problème : "+self.source_file+"\nevacuationPath : "+str(self.evacuationPath)+"\nedges : "+str(self.edges)
