#!/usr/bin/env python3

import os
import json
import argparse

def parse(file, activity):
    data = json.load(file)
    totalDistanceKm = 0.0
    totalDurationHour = 0.0
    for obj in data["timelineObjects"]:
        if "activitySegment" in obj:
            segment = obj["activitySegment"]
            if "activityType" in segment:
                activityType = segment["activityType"]
                if activityType == activity:
                    if "distance" in segment and "duration" in segment:
                        totalDistanceKm += segment["distance"] / 1000
                        duration = segment["duration"]
                        endTimestampMs = int(duration["endTimestampMs"]) 
                        startTimestampMs = int(duration["startTimestampMs"])
                        durationSec = (endTimestampMs - startTimestampMs) / 1000.0
                        totalDurationHour += durationSec / 3600
    return totalDistanceKm, totalDurationHour

def report(description, distanceKm, durationHour):
    average = distanceKm / durationHour
    print(f"{description:20}: {distanceKm:>8.1f} km, {durationHour:>6.1f} h, {average:>5.1f} km/h")    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--activity", help="The type of activity", default="CYCLING")
    args = parser.parse_args()

    totalDistance = 0.0
    totalDuration = 0.0
    for filename in os.listdir("."):
        if filename.endswith("json"):
            with open(filename, 'r') as infile:
                (distance, duration) = parse(infile, args.activity)
                totalDistance += distance
                totalDuration += duration
                report(filename, distance, duration)
    print("---")
    report("Total", totalDistance, totalDuration)

if __name__ == "__main__":
    main()

