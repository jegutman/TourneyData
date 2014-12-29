from getRatedEvents import *
for year in range(1991, 2013):
    for month in range(1, 13):
        print year, str(month).zfill(2)
        events = getRatedEvents(year, month, debug = True, force=True)
        for event in events:
            print "    ", " ".join(event)
