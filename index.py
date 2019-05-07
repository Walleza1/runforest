#!/usr/bin/env python3

from lib.Checker import Solution
from lib.Probleme import Probleme
from lib.Utils import Fifo

def main():
  #solution=Solution("Solutions/solution")
  #solution.solve()
  problem=Probleme("Instances/graphe-TD-sans-DL-data.full") # sparse_10_30_3_8_I.full")
  print("Problem:\n#####################\n" + str(problem))
  print("borne inférieure : " + str(problem.minimum("graphe-TD-sans-DL-data")) + "; borne supérieure : " + str(problem.maximum("graphe-TD-sans-DL-data")))

if __name__ == "__main__":
  main()
