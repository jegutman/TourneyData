from getRatedEvents import *
from getEventInfo import *
import time
import sys
#for year in range(1991, 2013):
count = 0
#for year in range(1991, 1992):
for year in range(2013, 1990, -1):
    for month in range(1, 13):
        print year, str(month).zfill(2)
        events = getRatedEvents(year, month, debug = True, force=False)
        for event in events:
            eventInfo = getEventInfo(event[0], delay=2.5, debug=True, onlyNew = True)
            #eventInfo = getEventInfo(event[0], delay=3, debug=True, onlyNew = False)
            if eventInfo:
                parseTournaments(eventInfo)
            print ""
            count += 1
            print "COUNT", count
            if count > 12000:
                sys.exit(1)
