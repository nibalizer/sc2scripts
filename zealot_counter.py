#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division

import os

import argparse
import sc2reader
from sc2reader.events import *


def zeroint(i):
    return 0

def init_analyzer():
    parser = argparse.ArgumentParser(
        description="""Print the Zealot stats on a replay"""
    )

    parser.add_argument('FILE', type=str, help="The file you would like to replay")
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

    # init variables
    zealots_made = 0
    zealots_died = 0

    # check if a protoss is playing
    races = [i.play_race for i in replay.players]
    if 'Protoss' not in races:
        return

    print("{0} on {1} at {2}".format(replay.type, replay.map_name, replay.start_time))
    for team in replay.teams:
        print(team)

    print("Winner {0}".format(replay.winner))
    print("Time {0}".format(replay.game_length))

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
    paths = init_analyzer()
    for replay in sc2reader.load_replays(paths, debug=True):
        analyze_replay(replay)
