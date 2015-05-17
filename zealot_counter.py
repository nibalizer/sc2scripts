#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division

import os

import argparse
import sc2reader
from sc2reader.events import *


def zeroint(i):
    return 0


def main():
    zealots_made = 0
    zealots_died = 0
    parser = argparse.ArgumentParser(
        description="""Print the Zealot stats on a replay"""
    )

    parser.add_argument('FILE', type=str, help="The file you would like to replay")
    args = parser.parse_args()

    paths = []
    if os.path.isdir(args.FILE):
        for root, dirs, files in os.walk(args.FILE):
            for name in files:
#                try:
                paths.append(os.path.join(root, name))
#                except:
#                    from pdb import set_trace; set_trace()
    else:
        paths = args.FILE

    print (paths)

    for replay in sc2reader.load_replays(paths, debug=True):
        print("Release {0}".format(replay.release_string))
        print("{0} on {1} at {2}".format(replay.type, replay.map_name, replay.start_time))
        print("")
        for team in replay.teams:
            print(team)
            for player in team.players:
                print("  {0}".format(player))

        print("\n--------------------------\n\n")

        # Allow specification of events to `show`
        # Loop through the events
        for event in replay.events:

            if event.name in ['UnitBornEvent', 'UnitInitEvent']:
                if 'Zealot' in str(event.unit):
                    zealots_made += 1

            if event.name in ['UnitDiedEvent']:
                if 'Zealot' in str(event.unit):
                    zealots_died += 1

        print ("Zealots made: {0}".format(zealots_made))
        print ("Zealots died: {0}".format(zealots_died))
        print ("Zealots that made it: {0}".format(zealots_made - zealots_died))


if __name__ == '__main__':
    main()
