#!/usr/bin/env python3

from lib.Checker import Solution
from lib.Probleme import Probleme
from lib.Utils import Fifo
import os, sys

def main(pathToFile,render=False):
  indir = "Instances"
  outdir = "Solutions"
  filename = pathToFile.replace(indir+"/","")

  instance_name = os.path.splitext(filename)[0]
  outfile = outdir + "/" + instance_name[:-1] + "sol"
  problem = Probleme(indir + "/" + filename)

  print("Borne supérieure : " + str(problem.maximum(outfile + ".max.txt", True)))
if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage {} pathToInstance".format(sys.argv[0]))
    sys.exit(1)
  main(sys.argv[1])
