#!/usr/bin/env python

import sys

# For each accident, output make/year as key, 1 as value.

for line in sys.stdin:

    vin, values = line.strip().split("\t")
    _, make, year = values.split(",")
    print make + year + "\t" + "1"
