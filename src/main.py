#! /usr/bin/env python

from World import *
# import cProfile


def main():
    world = World()
    world.run()

    return 0

if __name__ == '__main__':
    main()
    # cProfile.run('main()')