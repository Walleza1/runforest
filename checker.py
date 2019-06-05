#!/usr/bin/env python3

from lib.Checker import Solution
from lib.Probleme import Probleme
from lib.Utils import Fifo
import os, sys

def main(pathToFile, render=False):
  sol = Solution().load(pathToFile)
  if render:
    sol.probleme.renderPath()
  print("Solution is valid = {}".format(sol.verify()))


if __name__ == "__main__":
  if len(sys.argv) > 3 or len(sys.argv) <= 1:
    print("Usage {} pathToSolution [render]".format(sys.argv[0]))
    sys.exit(1)
  main(sys.argv[1], len(sys.argv) == 3)
