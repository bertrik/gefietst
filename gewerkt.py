#!/usr/bin/env python3

""" Parses google maps timeline JSON, counts days spent at work """

import os
import json
import argparse
import datetime


def parse(file, place):
    """ parses the given file for visits to the specified place """
    data = json.load(file)
    days = set()
    for obj in data["timelineObjects"]:
        if "placeVisit" in obj:
            visit = obj["placeVisit"]
            location = visit["location"]
            if "semanticType" in location:
                semantic_type = location["semanticType"]
                if semantic_type == place:
                    duration = visit["duration"]
                    start_time = int(duration["startTimestampMs"]) / 1000
                    date = datetime.date.fromtimestamp(start_time)
                    day = date.timetuple().tm_yday
                    days.add(day)
    return len(days)


def report(desc, num):
    """ reports days worked """
    print(f"{desc:20}: {num}")


def main():
    """ main entry point, report place visits summary to stdout """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--place",
                        help="Type of place visited, TYPE_WORK/HOME/etc",
                        default="TYPE_WORK")
    args = parser.parse_args()

    total_days = 0
    for filename in os.listdir("."):
        if filename.endswith("json"):
            with open(filename, 'r') as infile:
                num_days = parse(infile, args.place)
                report(filename, num_days)
                total_days += num_days
    print("---")
    report(f"Num days {args.place}", total_days)


if __name__ == "__main__":
    main()
