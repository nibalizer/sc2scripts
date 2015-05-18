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
        print(player.name)

        zs = [i for i in player.units if i.name == 'Zealot']
        zealots_made = len(zs)
        dead_zs = [i for i in zs if i.died_at is not None]
        zealots_died = len(dead_zs)

        print ("Zealots made: {0}".format(zealots_made))
        print ("Zealots died: {0}".format(zealots_died))
        print ("Zealots that made it: {0}".format(zealots_made - zealots_died))
        if (zealots_made - zealots_died) > 0:
            result_data["zealots_lived"] += 1
            result_data["total_zealots_lived"] += (zealots_made - zealots_died)
        else:
            result_data["zealots_all_died"] += 1


if __name__ == '__main__':
    result_data = {}
    result_data["zealots_lived"] = 0
    result_data["zealots_all_died"] = 0
    result_data["total_zealots_lived"] = 0
    paths = init_analyzer()
    for replay in sc2reader.load_replays(paths, debug=True):
        analyze_replay(replay, result_data)
    print ("###")
    print ("Number of games where zealots all died: ", result_data["zealots_all_died"])
    print ("Number of games where some zealots lived: {0}".format(result_data["zealots_lived"]))
    print ("Total number of zealots that lived: {0}".format(result_data["total_zealots_lived"]))
