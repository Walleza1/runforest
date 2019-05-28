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