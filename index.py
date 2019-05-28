#!/usr/bin/env python3

from lib.Checker import Solution
from lib.Probleme import Probleme
from lib.Utils import Fifo
import os

def main():
  indir = "Instances"
  outdir = "Solutions"

  sol = Solution().load("Solutions/sparse_10_30_3_10_sol.optimal.txt")
  print("Solution is valid? ", sol.verify())

  for filename in os.listdir(indir):
    if filename == "sparse_10_30_3_10_I.full":
      instance_name = os.path.splitext(filename)[0]
      outfile = outdir + "/" + instance_name[:-1] + "sol"
      problem = Probleme(indir + "/" + filename)

      print("#####################\nProblem '" + filename + "'")
      problem.compute_solution(instance_name, outfile + ".optimal.txt", False)

      #print("Borne inférieure : " + str(problem.minimum(outfile + ".min.txt", True)))
      #print("Borne supérieure : " + str(problem.maximum(outfile + ".max.txt", True)))
      print("\n\n")
if __name__ == "__main__":
  main()
