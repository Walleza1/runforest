import os, sys
from lib.Probleme import *
from lib.Utils import *

class Fuyards(object):
  def __init__(self,tBegin,tEnd,flow,nextArc,path):
    self.tBegin=tBegin
    self.tEnd=tEnd
    self.flow=flow
    self.nextArc = nextArc
    self.path=path

  def __repr__(self):
    return "Fuyards : {tbegin "+str(self.tBegin)+",tend "+str(self.tEnd)+", flow "+str(self.flow)+", nextArc "+str(self.nextArc)+" , path : "+str(self.path)+"}"

class GraphEdge(object):
  def __init__(self,arc):
    self.origin = arc.origin
    self.destination = arc.destination
    self.dueDate = arc.dueDate
    self.length = arc.length
    self.capacity = arc.capacity
    self.fifo=Fifo(self.length)

  def __repr__(self):
    return str(self.origin)+" -> "+str(self.destination)+" [ dueDate: "+str(self.dueDate)+", length : "+str(self.length)+", capacity : "+str(self.capacity)+",fifo : "+str(self.fifo)+"]"

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
      self.nodeIni = []
      for i in range(headerSize):
        temp = f.readline().split()
        self.nodeIni.append({"id":int(temp[0]),"rate":int(temp[1]),"tDebut":int(temp[2])})
        i+=1
      self.isValid = True if f.readline().strip().lower() == "valid" else False
      self.fObjectif = f.readline()
      self.timeCalc = float(f.readline())
      self.metadata = f.readlines()
      self.metadata = [ x.strip() for x in self.metadata ]

  def solve(self):
    t=0
    # Initialisation
    etat= { 'arc' : {}, 'node' : {} }
    # On crée un GraphEdge à partir de l'arc
    for arc in self.probleme.edges.items():
      etat['arc'][ arc[0] ] = GraphEdge(arc[1])
    # On initialise le noeud
    for node in self.nodeIni:
      etat['node'][ node['id'] ] = node
      # On prend tous les éléments & on les fou dans un tableau
      temp = [ x for x in self.probleme.evacuationPath if x.idNode == node['id']]
      # On vérifie que le tableau n'est pas vide
      if len(temp) == 0:
        continue
      # On initialise notre nouveau noeud
      obj = temp[0]
      etat['node'][ node['id'] ]['population'] = obj.pop
      etat['node'][ node['id'] ]['maxRate'] = obj.maxRate
      etat['node'][ node['id'] ]['path'] = obj.path
    # retirer avant d'ajouter dans le path ?
    while not(self.evacuationTermine(etat)):
      #for node in etat['node']:
      #  print(etat['node'][node])
      tempNode={}
      for arc in etat['arc']:
        # On prends la sortie de la fifo
        fuyard = etat['arc'][arc].fifo.head()
        if fuyard is not None:
          if fuyard.tEnd == t:
            # Retirer l'élément de la fifo
            etat['arc'][arc].fifo.pop()
            if fuyard.nextArc is None:
              continue 
            # On prends le prochain arc 
            arcObj = etat['arc'][ fuyard.nextArc ]
#            print(arcObj)
#            print(etat['arc'][arc])
            # Vérifie qu'on a déjà ajouter le node dans le temp 
            try:
              # Si déjà présent
              alreadyIn=tempNode[ fuyard.nextArc[0] ][1]
              # On ajoute le flow actuel à celui déjà présent
              alreadyIn.flow += fuyard.flow
            except KeyError:
              # Calcul le nextArc (vérifie qu'on est pas out of bound )
              if len(fuyard.path) > fuyard.path.index(fuyard.nextArc)+1:
                nextArc=fuyard.path[fuyard.path.index(fuyard.nextArc)+1]
              else:
                # Si on est out of bound (nextArc is None)
                nextArc=None
              # On crée un nouvel ensemble de fuyards
              alreadyIn=Fuyards(t,(t+arcObj.length),fuyard.flow,nextArc,fuyard.path)
            # On insert le node (nouveau ou pas) dans le dict
            tempNode[ fuyard.nextArc[0] ]=(fuyard.nextArc,alreadyIn)
      for departNode in tempNode:
        # On prends l'arc où ranger le foyard
        if etat['arc'][ tempNode[departNode][0] ].capacity > tempNode[departNode][1].flow:
          etat['arc'][ tempNode[departNode][0] ].fifo.push(tempNode[departNode][1])
        else:
          print("Not possible")
      # Parcours des arcs terminé donc on insert les nouveaux nodes de fuyards
      # Quand l'évacuation d'un noeud a commencé
      # On évacue au rate décidé. 
      # On push un groupe de fuyard
      for node in etat['node']:
        if etat['node'][node]['tDebut'] <= t :
          if etat['node'][node]['population'] > 0:
            etat['node'][node]['population']-=etat['node'][node]['rate']
            temp=Fuyards(t,t+(etat['arc'][ etat['node'][node]['path'][0] ].length),etat['node'][node]['rate'], etat['node'][node]['path'][1],etat['node'][node]['path'])
            etat['arc'][etat['node'][node]['path'][0] ].fifo.push(temp)
      t+=1
      PrintInColor.red([etat['arc'][x].fifo.isEmpty() for x in etat['arc']])
      PrintInColor.blue([etat['node'][x]['population'] for x in etat['node']])
    return etat

  def evacuationTermine(self,etat):
    for node in etat['node']:
      if (etat['node'][node]['population'] > 0):
        return False
    for arc in etat['arc']:
      if not(etat['arc'][arc].fifo.isEmpty()):
        return False
    return True
      
  def __repr__(self):
    return "File : " + str(self.file) + "\nProbleme : " + str(self.probleme) + "\n"

