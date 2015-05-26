#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division

import collections

import argparse
import sc2reader
from sc2reader.events import *


def main():
    players = {}
    parser = argparse.ArgumentParser(
        description="""Parse replay and drop immediately to a debug shell"""
    )

    parser.add_argument('FILE', type=str, help="The file you would like to replay")
    args = parser.parse_args()

    for filename in sc2reader.utils.get_files(args.FILE):
        replay = sc2reader.load_replay(filename, debug=True)
        r = replay
        from pdb import set_trace; set_trace()
        print("\n--------------------------\n\n")



if __name__ == '__main__':
    main()
