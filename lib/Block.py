class Block(object):
  def __init__(self,tBegin,tEnd,flow,NodeOriginId,temp=False):
    self.tBegin=tBegin
    self.tEnd=tEnd
    self.flow=flow
    self.temp=temp
    self.nodeOrigin=NodeOriginId

  def __repr__(self):
    return "Block : [ tBegin :{}, tEnd :{}, flow :{}, origin:{} ]".format(self.tBegin,self.tEnd,self.flow,self.nodeOrigin)
