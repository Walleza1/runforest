#!/usr/bin/env python3

from lib.Checker import Solution
from lib.Probleme import Probleme
from lib.Utils import Fifo
import os

def main():
  #solution=Solution("Solutions/solution")
  #solution.solve()

  #problem=Probleme("Instances/graphe-TD-sans-DL-I.full") # sparse_10_30_3_8_I.full")
  #print("Problem:\n#####################\n" + str(problem))
  #print("borne inférieure : " + str(problem.minimum("Solutions/graphe-TD-sans-DL-sol.min.txt")) + "; borne supérieure : " + str(problem.maximum("Solutions/graphe-TD-sans-DL-sol.max.txt")))

  indir = "Instances"
  outdir = "Solutions"
  for filename in os.listdir(indir):
    outfile = outdir + "/" + os.path.splitext(filename)[0][:-1] + "sol"
    problem = Probleme(indir + "/" + filename)

    print("#####################\nProblem '" + filename + "'")
    print("Borne inférieure : " + str(problem.minimum(outfile + ".min.txt", True)))
    print("Borne supérieure : " + str(problem.maximum(outfile + ".max.txt", True)))
    print("\n\n")

if __name__ == "__main__":
  main()
