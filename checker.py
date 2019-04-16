#!/usr/bin/env python3

import os, sys
import Probleme

def readSolutionFile(source_file):
  with open(source_file) as f:
    content=f.readlines()
    # Verifier que le fichier existe
    if not(os.path.isfile('Instances/'+content[0].replace("\n","")+".full")):
      print("Error file unknown")
      exit(1)
    
def main():
  readSolutionFile("solution")


if __name__ == "__main__":
  main()
