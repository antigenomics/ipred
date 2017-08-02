#!/usr/bin/python

import argparse
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help = 'The name of the file to process')
    args = parser.parse_args()

    f = args.file
    i = 0

    with open(f, 'r') as file:
        for line in file:
            if line.startswith("--"):
                i += 1
            else:
                print(line)
    eprint("{0} --- lines were in the original file".format(i))
