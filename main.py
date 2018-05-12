#! /usr/bin/env python

from World import *


def main():
    # world = World()
    # world.run()

    f = open("test.txt", "r")
    contents = f.readlines()
    print (len(contents))



if __name__ == '__main__':
    main()