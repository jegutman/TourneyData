
import re, sys
filename = 'Tdata.dat'
if len(sys.argv) > 1:
    filename = sys.argv[1]
data = open(filename)
lastid = "            "
for line in data:
    line = line.replace('\n', '')
    if len(line) == 0:
        continue
    tmp = re.split(' *', line)
    eventid = tmp[0]
    localPct = float(tmp[-1]) / 100.
    players = int(tmp[-2])
    state = tmp[-3]
    city = tmp[-4]
    eventName = ' '.join(tmp[1:-2])
    distant = int(players * (1-localPct))
    #if distant > 40 or 'AUSTIN' in eventName or 'ROUND ROCK' in eventName:
    if (distant > 30 and localPct < 0.35) or (distant > 100 and localPct < 0.45):
        if 'ELEMENTARY' not in eventName and 'GRADE' not in eventName and 'KIDS' not in eventName and 'SCHOLASTIC' not in eventName and 'SCHOOL' not in eventName and 'GIRLS' not in eventName and 'K-12' not in eventName and 'REGION' not in eventName:
            if lastid[4:6] != eventid[4:6]:
                print ""
                lastid = eventid
            print "%20s %70s %20s" % (eventid, eventName, players), distant
