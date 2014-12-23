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
    for res, rating in getPlayerTourneyHistory2(pid, t, s):
        if res[0] not in results:
            results[res[0]] = []
        results[res[0]].append(res)
        overall += [res]

resultItems = sorted(results.items(), key=lambda x:len(x[1]))
#print max(results.items(), key=lambda x:len(x[1]))
for i in resultItems:
    wins = len([d for a,b,c,d,e in i[1] if d == 'W'])
    draws = len([d for a,b,c,d,e in i[1] if d == 'D'])
    losses = len([d for a,b,c,d,e in i[1] if d == 'L'])
    if wins + draws + losses < 2:
        continue
    print "%10s %20s" % (i[1][1][0], i[1][1][1]), "%s-%s-%s" % (wins, losses, draws), [(j,k,l) for [a,b,j,k,l] in i[1]]
    #print wins
    #print i[1][1][1], len(i[1]), [(j,k,l) for [a,b,j,k,l] in i[1]]
       
    

