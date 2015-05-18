#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals,
                        division)

import os

import argparse
import sc2reader


def init_analyzer():
    parser = argparse.ArgumentParser(
        description="""Print the Zealot stats on a replay"""
    )

    parser.add_argument('FILE', type=str,
                        help="The file you would like to replay")
    args = parser.parse_args()

    paths = []
    if os.path.isdir(args.FILE):
        for root, dirs, files in os.walk(args.FILE):
            for name in files:
                paths.append(os.path.join(root, name))
    else:
        paths = args.FILE
    return paths


def analyze_replay(replay):

    # check if a protoss is playing
    races = [i.play_race for i in replay.players]
    if 'Protoss' not in races:
        return

    print("{0} on {1} at {2}".format(replay.type,
                                     replay.map_name, replay.start_time))
    for team in replay.teams:
        print(team)

    print("Winner {0}".format(replay.winner))
    print("Time {0}".format(replay.game_length))

    for player in replay.players:
        # bail if this player is not Protoss
        if player.play_race != 'Protoss':
            continue

        zs = [i for i in player.units if i.name == 'Zealot']
        zealots_made = len(zs)
        dead_zs = [i for i in zs if i.died_at is not None]
        zealots_died = len(dead_zs)


        print ("Zealots made: {0}".format(zealots_made))
        print ("Zealots died: {0}".format(zealots_died))
        print ("Zealots that made it: {0}".format(zealots_made - zealots_died))


if __name__ == '__main__':
    paths = init_analyzer()
    for replay in sc2reader.load_replays(paths, debug=True):
        analyze_replay(replay)
