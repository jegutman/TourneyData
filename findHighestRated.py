import sys, os, re, datetime
import subprocess

def getRating(uscfId):
    filename = '~jgutman/Dropbox/workspace/TourneyDataRepo/uscfRatings'
    filename = os.path.expanduser(filename)
    tmpfile = '~jgutman/Dropbox/workspace/TourneyDataRepo/onerating'
    filename = os.path.expanduser(tmpfile)
    lookup = subprocess.Popen(["grep", '%(uscfId)s' % locals(), filename], stdout=subprocess.PIPE).communicate()
    if not lookup[0]:
        #try:
        #    os.system('grep %(uscfId)s %(filename)s' % locals()
        #except:
        command = ['wget', '-O', tmpfile, 'http://www.uschess.org/msa/thin.php?%(uscfId)s' % locals()]
        print "Getting Player Info: %(uscfId)s" % locals()
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        data = open(tmpfile)
        playerinfo = {}
        for line in data:
            if '<input' not in line:
                continue
            field = re.search('name=[a-z0-9_]*', line)
            value = re.search("value='.*'", line)
            field = field.group(0).replace('name=', '')
            value = value.group(0).replace('value=', '')
            value = value.replace("'", '')
            playerinfo[field] = value
        rating = re.search('^[0-9]*', playerinfo['rating1']).group(0)
        fide = playerinfo['rating4'].split(' ')[0]
        name = playerinfo['memname']
        os.system('echo "%(uscfId)s,%(name)s,%(rating)s,%(fide)s" >> %(filename)s' % locals())
    else:
        name, rating, fide = lookup[0].replace('\n', '').split(',')[1:]
    if rating == '':
        rating = 0
    return name, int(rating), fide

#print getRating(12880989)

#sys.exit(1)

EXCLUDED_TOURNAMENTS = ['201309116302']
tournamentId = '201301065832'
def findHighestRated(tournamentId):
    assert False, "function depricated"
    filename = '~jgutman/Dropbox/workspace/TourneyDataRepo/tourneyInfo/tourneyInfo-%(tournamentId)s.1' % locals()
    filename = os.path.expanduser(filename)
    #print 'wget "http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.1" -O %(filename)s' % locals()
    url = "http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.1" % locals()
    args = ['wget', '-O', filename, url]
    subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print "Getting Info for: %(tournamentId)s.1" % locals()
    data = open(filename)
    active = False
    relevant = []
    players = []
    for line in data:
        if '<pre>' not in line and not active:
            continue
        if '<pre>' in line:
            active = True
            continue
        if '</pre>' in line:
            break
        relevant.append(line)
    for line in relevant:
        a = re.search('MbrDtlMain.php\?[0-9]{8}', line)
        if a:
            playerId = a.group(0)
            playerId = playerId.replace('MbrDtlMain.php?', '')
            playerInfo = getRating(playerId)
            players.append(playerInfo)

    players.sort(key=lambda a:a[1], reverse=True)
    return players[0]

import time

def findHighestRated2(tournamentId):
    filename = '~jgutman/Dropbox/workspace/TourneyDataRepo/tourneyInfo/tourneyInfo-%(tournamentId)s.1' % locals()
    filename = os.path.expanduser(filename)
    #print 'wget "http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.1" -O %(filename)s' % locals()
    url = "http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.1" % locals()
    try:
        data = open(filename)
    except:
        args = ['wget', '-O', filename, url]
        print "Getting Info for: %(tournamentId)s.1" % locals()
        time.sleep(3)
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        data = open(filename)
    if tournamentId == '201412043252': print "LINE:", data
    active = False
    relevant = []
    players = []
    for line in data:
        if '<pre>' not in line and not active:
            continue
        if '<pre>' in line:
            active = True
            continue
        if '</pre>' in line:
            break
        relevant.append(line)
    for line in relevant:
        a = re.search('MbrDtlMain.php\?[0-9]{8}', line)
        if a:
            playerId = a.group(0)
            playerId = playerId.replace('MbrDtlMain.php?', '')
        nameSearch = re.search('MbrDtlMain.php\?[0-9]{8}>.* .*<', line)
        if nameSearch and a:
            name = nameSearch.group(0)
            name = name.split('>')[1].replace('<', '')
        b = re.search('-> ?[0-9]{2,4}', line)
        if b:
            rating = b.group(0)
            rating = int(rating.replace('->', ''))
            players.append((playerId, name, rating))
    if tournamentId == '201412043252': assert False, players
    players.sort(key=lambda a:a[2], reverse=True)
    if not players:
        print "NO PLAYERS in %(tournamentId)s" % locals()
        players = [(None, None, None)]
    return players[0]

def findAvgRating(tournamentId):
    filename = '~jgutman/Dropbox/workspace/TourneyDataRepo/tourneyInfo/tourneyInfo-%(tournamentId)s.1' % locals()
    filename = os.path.expanduser(filename)
    url = "http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.1" % locals()
    try:
        data = open(filename)
    except:
        args = ['wget', '-O', filename, url]
        print "Getting Info for: %(tournamentId)s" % locals()
        time.sleep(3)
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        data = open(filename)
    active = False
    relevant = []
    players = []
    for line in data:
        if '<pre>' not in line and not active:
            continue
        if '<pre>' in line:
            active = True
            continue
        if '</pre>' in line:
            break
        relevant.append(line)
    for line in relevant:
        a = re.search('MbrDtlMain.php\?[0-9]{8}', line)
        if a:
            playerId = a.group(0)
            playerId = playerId.replace('MbrDtlMain.php?', '')
        nameSearch = re.search('MbrDtlMain.php\?[0-9]{8}>.* .*<', line)
        if nameSearch and a:
            name = nameSearch.group(0)
            name = name.split('>')[1].replace('<', '')
        b = re.search('-> ?[0-9]{2,4}', line)
        if b:
            rating = b.group(0)
            rating = int(rating.replace('->', ''))
            preRate = re.search('R: *[0-9]+', line)
            if preRate:
                preRate = int(preRate.group(0).replace('R:', '').replace(' ', ''))
                if round(rating - 49.9, -2) - round(preRate - 49.9, -2) >= 200 and preRate > 900:
                    prov = 'P' if re.search('R: *[0-9]+P', line) else ''
                    if prov == 'P' and not re.search('R: *[0-9]+P[0-9]{2}', line):
                        pass
                    else:
                        print "JUMP:",  round(rating - 49.9, -2) - round(preRate - 49.9, -2) - 100, prov, rating, preRate, name, tournamentId
                    pass
            players.append((playerId, name, rating))
    if not players:
        print "NO PLAYERS in %(tournamentId)s" % locals()
        players = [(None, None, None)]
        return
        print "RELEVANT", relevant
    #print players
    #print sum([p[2] for p in players]) , len(players)
    try:
        return sum([p[2] for p in players]) / len(players)
    except:
        assert False, players

def allResultsFromTournament(tournamentId):
    matchupList = [{}]
    filename = '~jgutman/Dropbox/workspace/TourneyDataRepo/tourneyInfo/tourneyInfo-%(tournamentId)s.1' % locals()
    filename = os.path.expanduser(filename)
    page = 1
    if '201006130511' == tournamentId:
        page = 3
    url = "http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.%(page)s" % locals()
    try:
        data = open(filename)
    except:
        args = ['wget', '-O', filename, url]
        print "Getting Info for: %(tournamentId)s" % locals()
        time.sleep(3)
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        data = open(filename)
    for line in data:
        #if 'RAUF' in line:
            #print line
        mus = re.search('(\|[WDLBHFUX][0-9 ]{4})+', line)
        mus2 = re.search('(\|[WDL][0-9 ]{3}[0-9]{1})+', line)
        if mus and mus2:
            matchups = mus.group(0)[1:].split('|')
            #print "Mline: ", line
            pairingId = re.search('[0-9]{1,4}</a> \|', line).group(0).replace('</a> |', '')
            name = re.search('\?[0-9]{8}>[A-Z ]+', line).group(0)[10:]
            usId = re.search('\?[0-9]{8}>', line).group(0)[1:9]
            #print "PID:", pairingId
        if len(matchupList) > 2 and not mus2 and mus:
            #assert False, line
            matchups = mus.group(0)[1:].split('|')
            #print "Mline: ", line
            pairingId = re.search('[0-9]{1,4}</a> \|', line).group(0).replace('</a> |', '')
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
            postRating = int(re.search('-> *[0-9]+', line).group(0).replace('->', '').replace(' ', ''))
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
    data.close()
    return matchupList
            
def getPlayerTourneyHistory2(uscfId, tournamentId, section):
    matchupList = [{}]
    page = section
    filename = '~jgutman/Dropbox/workspace/TourneyDataRepo/tourneyInfo/tourneyInfo-%(tournamentId)s.%(page)s' % locals()
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
            #print tournamentId, 
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

def getPlayerHistory(uscfId):
    page = 1
    tourneys = []
    ood = False
    for page in range(1,10):
        filename = '~jgutman/Dropbox/workspace/TourneyDataRepo/playerInfo/playerInfo-%(uscfId)s.%(page)s' % locals()
        filename = os.path.expanduser(filename)
        #print datetime.datetime.today().strftime('%s.%f')
        if ood:
            break
        try:
            if True or float(datetime.datetime.today().strftime('%s.%f')) - os.path.getmtime(filename) < 86400:
                data = open(filename)
            else:
                print "FILE OUT OF DATE", float(datetime.datetime.today().strftime('%s.%f')) - os.path.getmtime(filename)
                ood = True
                raise IOException
        except:
            url = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?%(uscfId)s.%(page)s" % locals()
            args = ['wget', '-O', filename, url]
            subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            time.sleep(2)
            print "...Getting Player History %(uscfId)s" % locals()
            data = open(filename)
        count = -1
        for line in data:
            ratingType = re.search('<td width=160> ?[0-9]{3,4}', line)
            if not ratingType and count >= 0:
                count += 1
            else:
                if count == 0:
                    tourneys.append((t, section, name)) ### move
                    count = -1
            t = re.search('XtblMain.php\?[0-9]{12}-', line)
            if t:
                t = t.group(0)[-13:-1]
            n = re.search('%(uscfId)s>.*</a>' % locals(), line)
            if t and n:
                name = n.group(0).replace('</a>', '').replace('>', '').replace(uscfId, '')
            section = re.search('<small>[0-9]*:', line)
            if section:
                section = section.group(0).replace('<small>', '').replace(':', '')
                count = 0
                #assert False, count
    return tourneys

def getPlayerTourneyHistory(uscfId, tournamentId, section):
    section = str(section)
    while len(section) < 3:
        section = '0' + section
    filename = '~jgutman/Dropbox/workspace/TourneyDataRepo/playerInfo/%(tournamentId)s-%(section)s-%(uscfId)s' % locals()
    filename = os.path.expanduser(filename)
    try:
        data = open(filename)
    except:
        url = 'http://www.uschess.org/msa/XtblPlr.php?%(tournamentId)s-%(section)s-%(uscfId)s' % locals()
        args = ['wget', '-O', filename, url]
        print "Getting Player Tournament History %(tournamentId)s %(uscfId)s" % locals()
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        time.sleep(2)
        data = open(filename)
    rating = None
    matches = []
    count = 0
    for line in data:
        r = re.search('^&nbsp;  ?[0-9]{3,4}', line)
        if r:
            rating = r.group(0).replace('&nbsp;', '').replace(' ' , '')
        memberId = re.search('MbrDtlMain.php\?[0-9]{8}>.*</a>', line)
        res = re.search('^[WLDHBF] +[0-9]{1,4}', line)
        if res:
            result = res.group(0)[0]
        if memberId:
            memberId = memberId.group(0).replace('MbrDtlMain.php?', '').replace('</a>', '')
            memberId, name = memberId.split('>')
            if memberId == str(uscfId):
                continue
                result = None
            matches.append((memberId, name, rating, result, tournamentId))
    return matches

def calcPR(results, playerRating):
    pr = 0
    for pid, name, rating, res, tid in results:
        rating = int(rating)
        if res == 'W':
            rating = max(rating, playerRating - 400)
        if res == 'L':
            rating = min(rating, playerRating + 400)
        res = 1 if res == 'W' else (-1 if res == 'L' else 0)
        pr += rating + res * 400
        #if rating + res * 400 < 2000:
            #print results
    #print pr / len(results), len(results)
    if len(results) == 0:
        assert False, results
    return pr / len(results), len(results)
