from collections import deque

class PrintInColor:
  RED = '\033[91m'
  GREEN = '\033[92m'
  BLUE = '\033[34m'
  YELLOW = '\033[93m'
  LIGHT_PURPLE = '\033[94m'
  PURPLE = '\033[95m'
  END = '\033[0m'

  @classmethod
  def red(cls, s, **kwargs):
    print(cls.RED + str(s) + cls.END, **kwargs)
  
  @classmethod
  def green(cls, s, **kwargs):
    print(cls.GREEN + str(s) + cls.END, **kwargs)

  @classmethod
  def yellow(cls, s, **kwargs):
    print(cls.YELLOW + str(s) + cls.END, **kwargs)

  @classmethod
  def lightPurple(cls, s, **kwargs):
    print(cls.LIGHT_PURPLE + str(s) + cls.END, **kwargs)

  @classmethod
  def purple(cls, s, **kwargs):
    print(cls.PURPLE + str(s) + cls.END, **kwargs)

  @classmethod
  def blue(cls, s, **kwargs):
    print(cls.BLUE + str(s) + cls.END, **kwargs)

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

  def isEmpty(self):
    return len(self.fifo) ==0

  def __repr__(self):
    return "Fifo : "+str(self.fifo)
