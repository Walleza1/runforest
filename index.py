#!/usr/bin/env python3

from lib.Checker import Solution
from lib.Probleme import Probleme
from lib.Utils import Fifo

def main():
  solution=Solution("Solutions/graphe-TD-sans-DL-sol.txt")
  solution.solve()

if __name__ == "__main__":
  main()
