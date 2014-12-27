def getEventsFromMonth(month, year, debug=False):
    if debug:
        print "looking up events for %(month)s/%(year)s" % locals()

    datePrefix = '%(year)s%(month)s' % locals()
    filename = '~jgutman/Dropbox/TourneyDataRepoRepo/ratedlist/ratedlist%(year)s%(month)s' % locals()
    filename = os.path.expanduser(filename)
    try:
        data = open(filename)
    except:
        print "getting events for %(month)s/%(year)s" % locals()
        command = 'wget http://www.uschess.org/datapage/events-rated.php --post-data "month=%(month)s/%(year)s&states=AL%%20AK%%20AS%%20AZ%%20AR%%20CA%%20CO%%20CT%%20DE%%20DC%%20FL%%20GA%%20GU%%20HI%%20ID%%20IL%%20IN%%20IA%%20KS%%20KY%%20LA%%20ME%%20MD%%20MH%%20MA%%20MI%%20FM%%20MN%%20MS%%20MO%%20MT%%20NE%%20NV%%20NH%%20NJ%%20NM%%20NY%%20NC%%20ND%%20MP%%20OH%%20OK%%20OR%%20PW%%20PA%%20PR%%20RI%%20SC%%20SD%%20TN%%20TX%%20UT%%20VT%%20VA%%20VI%%20WA%%20WV%%20WI%%20WY" -O %(filename)s' % locals()
        #print command
        subprocess.Popen(command.split(' '))

def parseEvent(moth, year, debug=False):
    filename = '~jgutman/Dropbox/TourneyDataRepoRepo/ratedlist/ratedlist%(year)s%(month)s' % locals()
    filename = os.path.expanduser(filename)
        data = open(filename)
    for line in data:
        #print line
        line = line.replace('\n', '')
        line = line.replace('&nbsp', '')
        line = line.replace(';', '')
        #if datePrefix in line:
        if True:
            #if 'TX' in line:
                #print line
                #assert False
            for i in line.split('</tr>'):
                #print i
                i = i.replace('<tr>', '')
                i = i.replace('<td>', '')
                
                i = [j for j in i.split('</td>') if j]
                #print len(i)
                if len(i) != 7:
                    continue
                i[0] = i[0].split('>')[1].split('<')[0]
                #print i
                eventId, numDays, eventName, city, state, players, localPct = i
                #if city == 'AUSTIN' and state == 'TX':
                #print state
                playerInfo = findHighestRated2(eventId)
                if state == 'TX' and city == 'AUSTIN':
                    playerInfo = findHighestRated2(eventId)
                    print playerInfo
                    #if playerInfo[2] > 2150:
                    #    print i, playerInfo
                if state != argState and argState != '':
                    continue
                #avgRating = findAvgRating(eventId)
                #if int(i[-2]) < 30:
                #    continue
                if argState:
                    print i
                else:
                    if state not in counts:
                        counts[state] = 0
                    counts[state] += 1
