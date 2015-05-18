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


def analyze_replay(replay, result_data):

    for player in replay.players:
        # bail if this player is not Protoss

        nydus = [i for i in player.units if 'Nydus' in i.name]
        if len(nydus) > 0:

            print("{0} on {1} at {2}".format(replay.type,
                                             replay.map_name, replay.start_time))
            for team in replay.teams:
                print(team)

            print("Winner {0}".format(replay.winner))
            print("Time {0}".format(replay.game_length))
            print ("Created Nydus")
            result_data["nydus"] += len(nydus)


if __name__ == '__main__':
    result_data = {}
    result_data["nydus"] = 0
    paths = init_analyzer()
    for replay in sc2reader.load_replays(paths, debug=True):
        analyze_replay(replay, result_data)
    print ("###")
    print ("Nyduses Created", result_data["nydus"])
