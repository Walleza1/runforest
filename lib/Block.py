class Block(object):
  def __init__(self,tBegin,tEnd,flow,temp=False):
    self.tBegin=tBegin
    self.tEnd=tEnd
    self.flow=flow
    self.temp=temp

  def __repr__(self):
    return "Block : {tBegin :"+str(self.tBegin)+",tEnd :"+str(self.tEnd)+", flow "+str(self.flow)+"}"