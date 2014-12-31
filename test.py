from getRatedEvents import *
from getEventInfo import *
import time
#for year in range(1991, 2013):
count = 0
for year in range(1991, 1992):
    for month in range(1, 13):
        print year, str(month).zfill(2)
        events = getRatedEvents(year, month, debug = True, force=False)
        for event in events:
            eventInfo = getEventInfo(event[0])
            time.sleep(2)
            count += 1
            if count > 10:
                assert False
