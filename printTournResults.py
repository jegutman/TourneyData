from findHighestRated import *
from tmp2 import TIDS

#print res[1]
tournId = '201210211602'
for tournId in TIDS:
    bestPerf = 0
    bestPlayer = ''
    bestTourn = ''
    bestRating = 0
    results = allResultsFromTournament(tournId)
    for playerResult in results[1:]:
        opp = ''
        oppRate = ''
        pid = playerResult['pid']
        name = playerResult['name']
        rating = playerResult['rating']
        matches = playerResult['matches']
        #print '        ',pid, ' ',  name, rating
        total = 0
        tmpmatches = [(res, oid, color) for (res, oid, color) in matches if oid > 0]
        wins = len([(res, oid, color) for (res, oid, color) in matches if res == 'W'])
        losses = len([(res, oid, color) for (res, oid, color) in matches if res == 'L'])
        draws = len([(res, oid, color) for (res, oid, color) in matches if res == 'D'])
        if (wins == 0 or losses == 0) and draws == 0:
            continue
        try:
            perf, count = calcPR([(oid, results[oid]['name'], results[oid]['rating'], res, pid) for (res, oid, color) in tmpmatches if res in ('W', 'D', 'L') and oid > 0], rating)
        except:
            continue
        if perf > 2000 and count >= 6 and perf - rating > bestPerf - bestRating:
        #if count >= 5 and perf - rating > bestPerf - bestRating:
            bestPerf = perf
            bestRating = rating
            bestPlayer = name
            bestTourn = tournId
            
        #for match in matches:
        #    oppRate = ''
        #    res, oid, color = match
        #    if res in ('W', 'B', 'X'):
        #        score = 1.0
        #    elif res in ('H', 'D'):
        #        score = 0.5
        #    else:
        #        score = 0
        #    if oid != -1:
        #        opp = results[oid]['name']
        #        oppRate = results[oid]['rating']
        #    else:
        #        if res in ('B', 'H'):
        #            opp = 'BYE'
        #        if res == 'F':
        #            opp = 'FORFEIT'
        #        if res == 'X':
        #            opp = 'FORFEIT WIN'
        #        if res == 'U':
        #            opp = 'NOT PLAYED'
        #    total += score
        #    #print "%(opp)-40s %(oppRate)6s %(color)5s %(res)5s %(score)3.1f %(total)8.1f" % locals()
        
        
    print bestRating, bestPerf, bestPerf - bestRating, bestPlayer, bestTourn
