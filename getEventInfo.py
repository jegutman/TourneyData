import os,os.path,urllib2
from HTMLParser import HTMLParser
from collections import deque

def parseResult(lines):
    # parse last line
    playerId = None
    groupId  = None
    for line in lines:
        if 'uscfid' in line:
            playerId = line.split('=')[1]
        if 'groupId' in line:
            groupId = line.split('=')[1]
    if not playerId or not groupId:
        for line in lines:
            print line
        assert False
    result = lines[-1]
    matchline, colorline = result.split('\n')[:2]
    print playerId
    matchgroups = matchline.split('|')
    colorgroups = colorline.split('|')
    print len(matchgroups), matchgroups
    print len(colorgroups), colorgroups
    games = zip(matchgroups[1:], colorgroups[2:])
    print games
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
        playerIdBox = False
        def handle_starttag(self, tag, attrs):
            self.tagHistory.append(tag)
            if len(self.tagHistory) > 20:
                self.tagHistory.popleft()
            if tag == 'a':
                attrDict = dict(attrs)
                self.playerIdBox = False
                if str(tournamentId) in attrDict.get('href', []) and 'XtblPlr' in attrDict.get('href', []):
                    self.playerIdBox = True
                elif str(tournamentId) in attrDict.get('href', []):
                    self.possibleSections.append(attrDict['href'])
                elif 'MbrDtlMain' in attrDict.get('href', []):
                    self.dataHistory.append('uscfid='+attrDict['href'][-8:])
            if tag == 'tr':
                currentRow = []
        def handle_endtag(self, tag):
            if tag == self.tagHistory[-1]:
                pass
                #self.tagHistory.pop()
        def handle_data(self, data):
            if self.playerIdBox: 
                self.dataHistory.append('groupId='+data)
            self.dataHistory.append(data)
            if len(self.dataHistory) > 20:
                self.dataHistory.popleft()
            if '->' in data:
                #print len(data.split('\n'))
                resultLines = [self.dataHistory[i] for i in range(min(0, len(self.dataHistory)-6), len(self.dataHistory))]
                #print resultLines
                #print data
                if 'USCF' in data:
                    self.dataHistory.clear()
                    return
                something = parseResult(resultLines)
                self.dataHistory.clear()
                #print data
            #print data
            if len(self.tagHistory) < 1: 
                pass
                #print "NO TAG", data
                #assert False
            elif self.tagHistory[-1] == 'td':
                pass
                #print data
            pass
    parser = MyHTMLParser()
    parser.feed(f.read())

getEventInfo('201409018812', debug=True)
#getEventInfo('201410134032', debug=True)
#getEventInfo('201409216042', debug=True)
