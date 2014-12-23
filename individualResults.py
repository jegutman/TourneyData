import sys
from findHighestRated import *
pid = '12880989'
if len(sys.argv) > 1:
    pid = sys.argv[1]
tourneyInfo = getPlayerHistory(pid)
results = {}
overall = []
for t, s, n in tourneyInfo:
    if 'BLITZ' in n:
        #print n
        continue
    matches, rating = getPlayerTourneyHistory2(pid, t, s)
    print matches
    #assert False
        #assert False, t
    #print matches
    if len(matches) == 0:
        continue
        #print t
    if matches[0] not in results:
        results[matches[0]] = []
    results[matches[0]].append(matches)
    overall += [matches]

    #[('12537405', 'DARRYL L WEST', 1905, 'D', '201309146722.1'), ('13915520', 'ALEX LI', 1631, 'W', '201309146722.1'), ('13942431', 'EMILY QUYNH NGUYEN', 2000, 'W', '201309146722.1')]
    matches = [i for i in matches if i[-2] in ('W', 'D', 'L')]
    #print tmpmatches
    #if len(tmpmatches) == 0:
    #    assert False, (t)
    #tmp = [(oid, results[oid]['name'], results[oid]['rating'], res, pid) for (res, oid, color) in tmpmatches if res in ('W', 'D', 'L') and oid > 0]
    #if len(tmp) == 0:
    #    assert False, t
    perf, count = calcPR(matches, rating)
    if count >= 3:
        print t + '.' + s, rating, perf, perf - rating
