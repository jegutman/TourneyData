import os,os.path,urllib2
import re
from HTMLParser import HTMLParser
from collections import deque
import time
import datetime

class Section():
    def __init__(self, tournamentId, sectionId):
        self.results = []
        self.playerMap = {}
        self.tournamentId = tournamentId
        self.sectionId = sectionId

    def addPlayer(self, player):
        self.results.append(player)
        self.playerMap[player.getEventId()] = player

class Tournament():
    def __init__(self, tournamentId):
        self.sections = []
        self.tournamentId = tournamentId
        self.sectionId = 0

    def newSection(self):
        self.sections.append(Section(self.tournamentId, self.sectionId))
        self.sectionId += 1

    def addPlayer(self, player):
        self.sections[-1].addPlayer(player)

class Player():
    def __init__(self, playerId, uscfId, tournamentId):
        self.games = None
        self.name = None
        self.uscfId = uscfId
        self.playerId = playerId
        self.ratings = {}
        self.tournamentId = tournamentId
        pass

    def ratingChange(self, ratingType, pre, preprov, post, postprov):
        self.ratings[ratingType] = (pre, preprov, post, postprov)

    def getRatingChange(self):
        for ratingType in ('R', 'Q', 'B'):
            if ratingType in self.ratings:
                pre, preprov, post, postprov = self.ratings[ratingType]
                if (pre, preprov) == ('', 'Unrated'):
                    return ratingType, 'Unr', int(post)
                try:
                    int(pre)
                except:
                    print self.ratings
                    assert False, (pre, self.tournamentId, self.name)
                return ratingType, pre, post
        assert False, self.ratings.keys()

    def addGames(self, games):
        self.games = games
    
    def setName(self, name):
        self.name = name

    def getEventId(self):
        return self.playerId
    
    def getId(self):
        return self.uscfId

def parseTournaments(tournaments):
    print tournaments.tournamentId
    results = [parseSingleTournament(t) for t in tournaments.sections]

def parseSingleTournament(tournament):
    resultMap = { 'W' : 1, 'B' : 1, 'N' : 1, 'D' : 0.5, 'H' : 0.5, 'Z' : 0.5, 'R' : 0.5, 'F' : 0, 'X' : 0, 'L' : 0, 'U' : 0, '?' : 0, 'S' : 0}
    crosstable = {}
    for player in tournament.results:
        crosstable[player.getEventId()] = []
        if not player.name: print player.uscfId,
        matchups = []
        total = 0
        for pairing, color in player.games:
            tmp = re.split('  *', pairing.strip())
            if re.match('[WDL]\d+', tmp[0]):
                tmp = [tmp[0][0], tmp[0][1:]]
                #assert False, tmp
            if len(tmp) != 2: 
                if tmp[0] == '*****':
                    crosstable[player.getEventId()].append(('***', '***', ''))
                    #TODO: Understand this next part
                elif len(tmp[0]) == 0:
                    continue
                if len(tmp[0]) == 1:
                    if tmp[0][0] == '0':
                        continue
                    elif tmp[0][0] == 'E':
                        continue
                    elif tmp[0][0] in ('U', 'B', 'F', 'H', 'X', 'Z'):
                        tmp = list(tmp).append(0)
                        continue
                    elif tmp[0][0] in ('*', ):
                        tmp[0] = '*****'
                    else:
                        print "oddResult", tmp, tournament.tournamentId
                if len(tmp[0]) == 5 and re.match('[WDL]\d+', tmp[0]):
                    tmp = (tmp[0], tmp[1:])
            if tmp[0] == '*****':
                crosstable[player.getEventId()].append(('***', '***', ''))
            if len(tmp) == 2:
                if tmp[0][0] == '0':
                    continue
                if not re.match('\d+', tmp[1]):
                    tmp[1] = 0
                result, opponent = tmp
                try:
                    opponent = int(opponent)
                except:
                    assert False, (opponent, tournament.tournamentId, result, tmp, re.match('[WDL]\d*', tmp[0]))
                crosstable[player.getEventId()].append((opponent, result, color))
                if result not in resultMap: assert False, (tmp[0], player.tournamentId)
                total += resultMap[result]
            #    print player.games
            #    assert False, (tmp, len(tmp), player.getEventId(), player.getId())
        ratingType, pre, post = player.getRatingChange()
        print "%-30s" % player.name, "%s: %4s -> %4s" % (ratingType, pre, post), "%4s" % player.getEventId(), "   ", 
        for o, r, c in crosstable[player.getEventId()]:
            print "%-3s %-3s" % (r, o),
        print ""

def parseResult(lines, tournamentId):
    possibleResults = []
    # parse last line
    uscfId = None
    groupId  = None
    for line in lines:
        if 'uscfid' in line:
            uscfId = line.split('=')[1]
        if 'groupId' in line:
            groupId = line.split('=')[1]
        if 'playerName' in line:
            playerName = line.split('=')[1]
    if not uscfId or not groupId:
        for line in lines:
            print line
        assert False
    result = lines[-1]
    matchline, colorline = result.split('\n')[:2]
    matchgroups = matchline.split('|')
    colorgroups = [c.strip() for c in colorline.split('|')]
    games = [g for g in zip(matchgroups[1:], colorgroups[2:]) if len(g) == 2 and g[0]]
    score, norm = games[0]
    games = games[1:]
    for g in games:
        res = g[0].split(' ')[0]
        if res not in possibleResults:
            possibleResults.append(res)
    #print playerName, uscfId, groupId, games
    #print "%30s" % playerName, uscfId, groupId, len(games), games
    player = Player(groupId, uscfId, tournamentId) 
    player.addGames(games)
    player.setName(playerName)
    ratingChanges = [r for r in lines[-1].split('|') if '->' in r]
    for change in ratingChanges:
        m = re.search('([A-Z]): *(\d*)(.*)-> *(\d*)(.*)', change)
        ratingType, pre, preProvisional, post, postProvisional = m.groups()
        player.ratingChange(ratingType, pre, preProvisional, post, postProvisional)
        #print "%-30s" % playerName, m.groups()
    return player

def getEventInfo(tournamentId, force=False, debug=False, delay=2, onlyNew=False):
    year, month = tournamentId[:4], tournamentId[4:6]
    if debug:
        print year, month
    filenameWithSection = 'tourneyInfo/%(year)s/%(month)s/tourneyInfo-%(tournamentId)s.%(section)s'
    filename = 'tourneyInfo/%(year)s/%(month)s/tourneyInfo-%(tournamentId)s.0'
    section = 0
    if not os.path.isdir('tourneyInfo/%(year)s/' % locals()):
        os.system('mkdir -p tourneyInfo/%(year)s/' % locals())
    if not os.path.isdir('tourneyInfo/%(year)s/%(month)s/' % locals()):
        os.system('mkdir -p tourneyInfo/%(year)s/%(month)s/' % locals())
    if (not os.path.isfile(filename % locals()) and not os.path.isfile(filenameWithSection % locals())) or force:
        if delay > 0:
            print datetime.datetime.now().strftime('%H:%M:%S')
            print "SLEEPING for %s sec" % delay
            time.sleep(delay)
        if debug:
            print "not found %s" % (filename % locals())
            print 'fetching %(tournamentId)s' % locals()
        # get parent
        url = 'http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.0' % locals()
        #creating HTTP Req
        req = urllib2.Request(url)
        #time.sleep(3)
        for i in range(0,5):
            try:
                f = urllib2.urlopen(req, timeout=5)
                savefile = open(filename % locals(), 'w')
                savefile.writelines(f.read())
                savefile.close()
                break
            except:
                if i < 4:
                    continue
                else:
                    return None
                    
    else:
        if onlyNew:
            return None
        if debug:
            print "found %s" % filename % locals()
    f = open(filename % locals())

    class MyHTMLParser(HTMLParser):
        possibleSections = []
        tagHistory = deque()
        currentRow = []
        tournaments = Tournament(tournamentId)
        inTournament = False
        dataHistory = deque([])
        debug = None
        playerIdBox = False
        uscfIdBox = False
        lastActiveTag = [None]
        def handle_starttag(self, tag, attrs):
            if tag not in ('b', 'br'):
                self.lastActiveTag.append(tag)
            self.tagHistory.append(tag)
            if len(self.tagHistory) > 20:
                self.tagHistory.popleft()
            if tag == 'a':
                attrDict = dict(attrs)
                if str(tournamentId) in attrDict.get('href', []) and 'XtblPlr' in attrDict.get('href', []):
                    self.playerIdBox = True
                    self.debug = attrDict['href']
                elif str(tournamentId) in attrDict.get('href', []):
                    self.possibleSections.append(attrDict['href'])
                elif 'MbrDtlMain' in attrDict.get('href', []):
                    self.dataHistory.append('uscfid='+attrDict['href'][-8:])
                    self.uscfIdBox = True
            if tag == 'tr':
                currentRow = []
        def handle_endtag(self, tag):
            if tag == self.lastActiveTag[-1]:
                self.lastActiveTag = self.lastActiveTag[:-1]
            if tag == self.tagHistory[-1]:
                pass
                #self.tagHistory.pop()
            if tag == 'a':
                self.playerIdBox = False
                self.uscfIdBox = False
        def handle_data(self, data):
            if self.playerIdBox: 
                self.dataHistory.append('groupId='+data)
                if int(data) == 1:
                    self.tournaments.newSection()
            if self.uscfIdBox:
                self.dataHistory.append('playerName='+data)
            self.dataHistory.append(data)
            if len(self.dataHistory) > 20:
                self.dataHistory.popleft()
            rchange = re.search('-> *\d\d\d', data)
            #if '->' in data and self.lastActiveTag[-1] != 'a':
            if rchange:
                resultLines = [self.dataHistory[i] for i in range(min(0, len(self.dataHistory)-6), len(self.dataHistory))]
                if 'USCF' in data:
                    self.dataHistory.clear()
                    return
                player = parseResult(resultLines, tournamentId)
                self.tournaments.addPlayer(player)
                self.dataHistory.clear()
            if len(self.tagHistory) < 1: 
                pass
            elif self.tagHistory[-1] == 'td':
                pass
            pass
    parser = MyHTMLParser()
    parser.feed(f.read())
    #print len(parser.tournaments)
    return parser.tournaments
        

#getEventInfo('201409018812', debug=True)
#getEventInfo('201410134032', debug=True)
#getEventInfo('201409216042', debug=True)
#print possibleResults
