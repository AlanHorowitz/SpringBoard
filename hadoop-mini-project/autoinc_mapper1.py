#!/usr/bin/env python

import sys

# Output vin_number as key with incident_type, make and year as data.  Drop other columns.

for line in sys.stdin:

    cols = line.strip().split(",")
    key = cols[2]
    value = ",".join([cols[1], cols[3], cols[5]])
    print "%s\t%s" % (key, value)
