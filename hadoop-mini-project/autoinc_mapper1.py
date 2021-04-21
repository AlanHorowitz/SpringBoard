#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)

for line in sys.stdin:

    cols = line.strip().split(",")
    key = cols[2]
    value = ",".join([cols[1], cols[3], cols[5]])
    print '%s\t%s' % (key, value)
