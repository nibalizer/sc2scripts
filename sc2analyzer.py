#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division

import collections

import argparse
import sc2reader
from sc2reader.events import *


def zeroint(i):
    return 0;


def main():
    players = {}
    parser = argparse.ArgumentParser(
        description="""Step by step replay of game events; shows only the
        Initialization, Command, and Selection events by default. Press any
        key to advance through the events in sequential order."""
    )

    parser.add_argument('FILE', type=str, help="The file you would like to replay")
    parser.add_argument('--player', default=0, type=int, help="The number of the player you would like to watch. Defaults to 0 (All).")
    parser.add_argument('--bytes', default=False, action="store_true", help="Displays the byte code of the event in hex after each event.")
    parser.add_argument('--hotkeys', default=False, action="store_true", help="Shows the hotkey events in the event stream.")
    parser.add_argument('--cameras', default=False, action="store_true", help="Shows the camera events in the event stream.")
    args = parser.parse_args()

    for filename in sc2reader.utils.get_files(args.FILE):
        replay = sc2reader.load_replay(filename, debug=True)
        r = replay
        print("Release {0}".format(replay.release_string))
        print("{0} on {1} at {2}".format(replay.type, replay.map_name, replay.start_time))
        print("")
        for team in replay.teams:
            print(team)
            for player in team.players:
                print("  {0}".format(player))
                players[player.name] = collections.defaultdict(zeroint)

        print("\n--------------------------\n\n")



if __name__ == '__main__':
    main()
