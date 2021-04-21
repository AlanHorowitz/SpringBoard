#!/usr/bin/env python

import sys

# Output cumulative count as value for each Make/Year key

last_makeyear = None
total = 0

for line in sys.stdin:

    makeyear, count = line.strip().split("\t")
    count = int(count)

    if makeyear != last_makeyear:
        if last_makeyear != None:
            print last_makeyear + "\t" + str(total)
        last_makeyear = makeyear
        total = 0

    total += 1

print last_makeyear + "\t" + str(total)
