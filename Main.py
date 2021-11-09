from Scanner import Scanner
from Grammar import *
from Core import Core
import sys

def main():

  # Initialize the scanner with the input code file and data file
  S = Scanner(sys.argv[1])
  D = Scanner(sys.argv[2])

  # Calling the parser on the tokenized code
  root = Prog()
  root.parse(S)
  #root.print()

  # Calling the executor on the parsed tree
  root.execute(D)

if __name__ == "__main__":
    main()