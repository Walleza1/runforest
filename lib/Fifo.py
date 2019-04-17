from collections import deque

class Fifo(object):

  def __init__(self,sizeMax):
    self.fifo=deque([],sizeMax)

  def push(self,elmt):
    if (len(self.fifo) < self.fifo.maxlen):
      self.fifo.appendleft(elmt)
    else:
      print("Fifo full")


  def pop(self):
    ret = None
    try:
      ret=self.fifo.pop()
    except IndexError:
      ret = None
    return ret

  def head(self):
    ret=self.pop()
    if not(ret is None):
      self.fifo.append(ret)
    return ret

  def __repr__(self):
    return "Fifo : "+str(self.fifo)
