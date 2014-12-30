import os,os.path,urllib2
import re
from HTMLParser import HTMLParser
from collections import deque

possibleResults = []

class PlayerEvent():
    def __init__(self, playerId, uscfId):
        self.games = None
        self.uscfId = uscfId
        self.playerId = playerId
        self.ratings = {}
        pass

    def ratingChange(ratingType, pre, preprov, post, postprov):
        self.ratings[ratingType] = (pre, preprov, post, postprov)

def parseResult(lines):
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
    global possibleResults
    for g in games:
        res = g[0].split(' ')[0]
        if res not in possibleResults:
            possibleResults.append(res)
    #print playerName, uscfId, groupId, games
    #print "%30s" % playerName, uscfId, groupId, len(games), games
    playerResult = PlayerEvent(groupId, uscfId) 
    ratingChanges = [r for r in lines[-1].split('|') if '->' in r]
    for change in ratingChanges:
        m = re.search('([A-Z]): *(\d*)(.*)-> *(\d*)(.*)', change)
        ratingType, pre, preProvisional, post, postProvisional = m.groups()
        print m.groups()
    pass

def getEventInfo(tournamentId, force=False, debug=False):
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
        if debug:
            print "not found %s" % (filename % locals())
            print 'fetching %(tournamentId)s' % locals()
        # get parent
        url = 'http://www.uschess.org/msa/XtblMain.php?%(tournamentId)s.0' % locals()
        #creating HTTP Req
        req = urllib2.Request(url)
        #time.sleep(3)
        f = urllib2.urlopen(req)
        savefile = open(filename % locals(), 'w')
        savefile.writelines(f.read())
        savefile.close()
    else:
        if debug:
            print "found %s" % filename % locals()
    f = open(filename % locals())

    class MyHTMLParser(HTMLParser):
        possibleSections = []
        tagHistory = deque()
        currentRow = []
        tournaments = []
        inTournament = False
        dataHistory = deque([])
        debug = None
        playerIdBox = False
        uscfIdBox = False
        def handle_starttag(self, tag, attrs):
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
            if tag == self.tagHistory[-1]:
                pass
                #self.tagHistory.pop()
            if tag == 'a':
                self.playerIdBox = False
                self.uscfIdBox = False
        def handle_data(self, data):
            if self.playerIdBox: 
                self.dataHistory.append('groupId='+data)
            if self.uscfIdBox:
                self.dataHistory.append('playerName='+data)
            self.dataHistory.append(data)
            if len(self.dataHistory) > 20:
                self.dataHistory.popleft()
            if '->' in data:
                resultLines = [self.dataHistory[i] for i in range(min(0, len(self.dataHistory)-6), len(self.dataHistory))]
                if 'USCF' in data:
                    self.dataHistory.clear()
                    return
                something = parseResult(resultLines)
                self.dataHistory.clear()
            if len(self.tagHistory) < 1: 
                pass
            elif self.tagHistory[-1] == 'td':
                pass
            pass
    parser = MyHTMLParser()
    parser.feed(f.read())

#getEventInfo('201409018812', debug=True)
getEventInfo('201410134032', debug=True)
#getEventInfo('201409216042', debug=True)
print possibleResults
