#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)

for line in sys.stdin:

    vin, values = line.strip().split("\t")
    _, make, year = values.split(",")
    print(make + year + "\t" + "1")
