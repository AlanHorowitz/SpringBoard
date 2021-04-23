#!/usr/bin/env python

import sys


class GroupMaster:
    def __init__(self):
        self.vin = None
        self.accident_count = 0
        self.make = ""
        self.year = ""


group_master = GroupMaster()

# Run for end of every group
def flush(group_master):
    for _ in range(group_master.accident_count):
        key = group_master.vin
        value = ",".join(["A", group_master.make, group_master.year])
        print(f"{key}\t{value}")


def reset(group_master):
    group_master = GroupMaster()


for line in sys.stdin:

    vin, values = line.strip().split("\t")
    incident_type, make, year = values.split(",")
    if group_master.vin != vin:
        if group_master.vin != None:
            # write result to STDOUT
            flush(group_master)

        reset(group_master)
        group_master.vin = vin

    if incident_type == "I":
        group_master.make = make
        group_master.year = year
    elif incident_type == "A":
        group_master.accident_count += 1

flush(group_master)
