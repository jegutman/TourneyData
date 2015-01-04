from getRatedEvents import *
from getEventInfo import *
import time
import sys
#for year in range(1991, 2013):
count = 0
for year in range(1991, 2015):
    yearcount = 0
    for month in range(1, 13):
        monthcount = 0
        print year, str(month).zfill(2)
        events = getRatedEvents(year, month, debug = False, force=False)
        for event in events:
            count += 1
            yearcount += 1
            monthcount += 1
        print "MONTH COUNT", monthcount
    print " YEAR COUNT", yearcount
print "TOTAL", count
