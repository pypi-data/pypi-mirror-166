#!/usr/bin/env python

import argparse
#import cmd2
import os
import sys

import typer

# No arg

#def main():
#    print("Hello World")

# One arg

#def main(name: str):
#    print(f"Hello {name}")

# Two args
    
#def main(name: str, lastname: str):
#    print(f"Hello {name} {lastname}")
    
# Optional, bool

#def main(name: str, lastname: str, formal: bool = False):
#    if formal:
#        print(f"Good day Ms. {name} {lastname}.")
#    else:
#        print(f"Hello {name} {lastname}")
        
# Optional, 2nd arg

def main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        print(f"Good day Ms. {name} {lastname}.")
    else:
        print(f"Hello {name} {lastname}")

if __name__ == "__main__":
    typer.run(main)
