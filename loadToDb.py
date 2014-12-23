import sys, os, re, datetime
import subprocess

def getPlayerTourneyHistory2(uscfId, tournamentId, section):
    matchupList = [{}]
    page = section
    filename = '~jgutman/Dropbox/TourneyData/tourneyInfo/tourneyInfo-%(tournamentId)s.%(page)s' % locals()
    filename = os.path.expanduser(filename)
    url = "http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.%(page)s" % locals()
    playerPID = -1
    try:
        data = open(filename)
    except:
        args = ['wget', '-O', filename, url]
        print "Getting Info for: %(tournamentId)s.%(page)s" % locals()
        time.sleep(3)
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        data = open(filename)
    matchups = None
    players = None
    for line in data:
        if not players:
            players = re.search('nbsp; [0-9]* Players', line)
            if players:
                players = int(players.group(0)[5:-8])
        #if 'RAUF' in line:
            #print line
        mus = re.search('(\|[WDLBHFUX][0-9 ]{4})+', line)
        mus2 = re.search('(\|[WDL][0-9 ]{3}[0-9]{1})+', line)
        if mus and mus2:
            matchups = mus.group(0)[1:].split('|')
            #print "Mline: ", line
            try:
                pairingId = re.search('[0-9]{1,4}</a> \|', line).group(0).replace('</a> |', '')
            except:
                if players < 0.5 * int(matchups[0][1:]):
                    data.close()
                    return [], 0
                assert False, (tournamentId, line, mus2, mus, int(matchups[0][1:]))
            name = re.search('\?[0-9]{8}>[A-Z a-z\[\]]+', line).group(0)[10:]
            usId = re.search('\?[0-9]{8}>', line).group(0)[1:9]
            if uscfId in usId:
                playerPID = int(pairingId)
            #print "PID:", pairingId
                
        if len(matchupList) > 2 and not mus2 and mus and not matchups:
            #assert False, line
            matchups = mus.group(0)[1:].split('|')
            #print "Mline: ", line
            try:
                pairingId = re.search('[0-9]{1,4}</a> \|', line).group(0).replace('</a> |', '')
            except:
                assert False, (tournamentId, line, mus2, mus)
            name = re.search('\?[0-9]{8}>[A-Z ]+', line).group(0)[10:]
            usId = re.search('\?[0-9]{8}>', line).group(0)[1:9]
            colors = ['' for i in matchups]
            for i in range(0, len(matchups)):
                if matchups[i][0] in ('H', 'B', 'F', 'U', 'X', ''):
                    pairId = -1
                else:
                    #print line
                    #print matchups[i] == 'H'
                    #print "M:", matchups[i]
                    pairId = int(matchups[i][1:])
                matches.append((matchups[i][0], pairId, colors[i]))
            matchupList.append({'pid' : int(pairingId), 'name' : name, 'rating' : postRating, 'matches' : matches, 'uscfId' : usId})
            matchups = None
        colors = re.search('(\|[WB ]{5})+', line)
        if colors and matchups and not mus2:
            postRating = re.search('-> *[0-9]+', line)
            if postRating:
                postRating = int(postRating.group(0).replace('->', '').replace(' ', ''))
            else:
                postRating = 1500
            colors = colors.group(0)[1:].replace(' ', '').split('|')
            if len(colors) > len(matchups):
                colors = colors[1:]
            matches = []
            for i in range(0, len(matchups)):
                if matchups[i][0] in ('H', 'B', 'F', 'U', 'X', ''):
                    pairId = -1
                else:
                    #print line
                    #print matchups[i] == 'H'
                    #print "M:", matchups[i]
                    pairId = int(matchups[i][1:])
                matches.append((matchups[i][0], pairId, colors[i]))
            matchupList.append({'pid' : int(pairingId), 'name' : name, 'rating' : postRating, 'matches' : matches, 'uscfId' : usId})
            matchups = None
            #return
    if playerPID == -1:
        data.close()
        return [], 0
    else:
        matches = matchupList[playerPID]['matches']
        result = []
        for res, pairId, color in matches:
            if pairId == 0 or res in ('F', 'H', 'X', 'U'):
                continue
            oUsId = matchupList[pairId]['uscfId']
            oName = matchupList[pairId]['name']
            oRate = matchupList[pairId]['rating']
            result.append((oUsId, oName, oRate, res, tournamentId + '.' + page))
    #matches.append((memberId, name, rating, result, tournamentId))
    #return matchupList
    data.close()
    return result, matchupList[playerPID]['rating']
