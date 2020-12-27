#!/usr/bin/env python3

""" Parses google maps timeline JSON files and aggregates distance travelled by a activity """

import os
import json
import argparse

def parse(file, activity):
    """ parses the given file for activity segment of the given type """
    data = json.load(file)
    total_distance_km = 0.0
    total_duration_hour = 0.0
    for obj in data["timelineObjects"]:
        if "activitySegment" in obj:
            segment = obj["activitySegment"]
            if "activityType" in segment:
                activity_type = segment["activityType"]
                if activity_type == activity:
                    if "distance" in segment and "duration" in segment:
                        total_distance_km += segment["distance"] / 1000.0
                        duration = segment["duration"]
                        end_timestamp_ms = int(duration["endTimestampMs"])
                        start_timestamp_ms = int(duration["startTimestampMs"])
                        duration_sec = (end_timestamp_ms - start_timestamp_ms) / 1000.0
                        total_duration_hour += duration_sec / 3600
    return total_distance_km, total_duration_hour

def report(desc, distance_km, duration_hour):
    """ reports the description, distance, time and average one a line to stdout """
    average = distance_km / duration_hour
    print(f"{desc:20}: {distance_km:>8.1f} km, {duration_hour:>6.1f} h, {average:>5.1f} km/h")

def main():
    """ main entry point, parses arguments and report activity summary to stdout """
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--activity", help="The type of activity", default="CYCLING")
    args = parser.parse_args()

    total_distance = 0.0
    total_duration = 0.0
    for filename in os.listdir("."):
        if filename.endswith("json"):
            with open(filename, 'r') as infile:
                (distance, duration) = parse(infile, args.activity)
                report(filename, distance, duration)
                total_distance += distance
                total_duration += duration
    print("---")
    report("Total", total_distance, total_duration)

if __name__ == "__main__":
    main()
