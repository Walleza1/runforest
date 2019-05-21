#!/usr/bin/env python3

from lib.Checker import Solution
from lib.Probleme import Probleme
from lib.Utils import Fifo
import os

def main():
  indir = "Instances"
  outdir = "Solutions"
  for filename in os.listdir(indir):
    outfile = outdir + "/" + os.path.splitext(filename)[0][:-1] + "sol"
    problem = Probleme(indir + "/" + filename)

    problem.compute_solution(outfile + ".min.txt", True)

    print("#####################\nProblem '" + filename + "'")
    #print("Borne inférieure : " + str(problem.minimum(outfile + ".min.txt", True)))
    #print("Borne supérieure : " + str(problem.maximum(outfile + ".max.txt", True)))
    print("\n\n")

if __name__ == "__main__":
  main()
