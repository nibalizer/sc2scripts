#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals,
                        division)

import os
import math
import copy

import argparse
import sc2reader


def init_analyzer():
    parser = argparse.ArgumentParser(
        description="""Find Cannon Rushes"""
    )

    parser.add_argument('FILE', type=str,
                        help="The file you would like to replay")
    args = parser.parse_args()

    # deterimine if recursing through directory or using a single file
    paths = []
    if os.path.isdir(args.FILE):
        for root, dirs, files in os.walk(args.FILE):
            for name in files:
                paths.append(os.path.join(root, name))
    else:
        paths = args.FILE
    return paths


def analyze_replay(replay, result_data):

    cannon_rush = False
    for player in replay.players:
        # bail if this player is not Protoss

        cannons = [i for i in player.units if 'Cannon' in i.name]
        if len(cannons) > 0:

            print("{0} on {1} at {2}".format(replay.type,
                                             replay.map_name,
                                             replay.start_time))
            for team in replay.teams:
                print(team)

            print("Winner {0}".format(replay.winner))
            print("Time {0}".format(replay.game_length))
            result_data["cannons"] += len(cannons)

            # Detect cannon rush

            # See if cannons before nexus

            nexi = [i for i in player.units if i.name == 'Nexus' ]
            expo_start_time = nexi[1].started_at
            if cannons[0].started_at > expo_start_time:
                print ("Cannons started after expo, no cannon rush")
                continue

            # See if cannon is close to enemy starting position
            players_copy = copy.copy(replay.players)
            players_copy.remove(player)
            enemy_start_position = players_copy[0].units[15].location  # 15 becuase the first 14 are random init things
            cannon_pos = cannons[0].location
            x1,y1,x2,y2 = [ int(i) for i in  cannon_pos + enemy_start_position ]

            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)

            print ("Cannon Distance from enemy start " + str(distance))
            if distance < 65:
                print ("Cannon distance from ememy start lower than threshold(65)")
                print ("Cannon rush detected")
                cannon_rush = True
            else:
                print ("Cannon too far from enemy base, no cannon rush")
                continue

            # See if cannon made before 5 minutes
            for i in cannons:
                if i.started_at < (5 * 60 * replay.game_fps):
                    print ("Cannon started inside of 5 minutes, cannon rush detected")
                    cannon_rush = True

            # See if food is below 20
            player_stats_events = [i for i in replay.tracker_events if i.name == 'PlayerStatsEvent' and i.player.name == player.name]
            for i in sorted(cannons, key=lambda cannon: cannon.started_at):
                started_at = i.started_at
                # search stats events
                correct_stat_event_index = 0
                for index in range(len(player_stats_events)):
                    if started_at > player_stats_events[index].frame:
                        if started_at < player_stats_events[index+1].frame:
                            correct_stat_event_index = index
                            break

                food = player_stats_events[correct_stat_event_index].food_used
                if food < 20:
                    print("Cannon built when less than 20 food, cannon rush detected")
                    cannon_rush = True

    result_data["cannon_rush"] = cannon_rush


if __name__ == '__main__':
    result_data = {}
    result_data["cannons"] = 0
    result_data["cannon_rush"] = False
    result_data["cannon_rush_games"] = []
    paths = init_analyzer()
    for path in paths:
        replay = sc2reader.load_replay(path, debug=True)
        analyze_replay(replay, result_data)
        if result_data["cannon_rush"]:
            result_data["cannon_rush_games"].append(path)
    print ("###")
    print ("Cannons Created", result_data["cannons"])
    if result_data["cannon_rush"]:
        print ("Cannon Rush detected")

    print (" #### ")
    for i in result_data["cannon_rush_games"]:
        print ("Cannon rush in: " + i)

