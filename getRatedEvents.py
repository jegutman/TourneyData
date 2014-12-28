import subprocess

import os.path,urllib2
from HTMLParser import HTMLParser
#month, year = 12, 2014
def getRatedEvents(month, year, force=False, debug=False):
    month = str(month).zfill(2)
    filename = 'ratedlist/ratedlist-%(year)s%(month)s' % locals()
    if not os.path.isfile(filename) or force:
        if debug:
            print "not found %s" % filename
            print 'fetching %(year)s %(month)s' % locals()
        url  = 'http://www.uschess.org/datapage/events-rated.php'
        data = 'month=%(month)s/%(year)s&states=AL%%20AK%%20AS%%20AZ%%20AR%%20CA%%20CO%%20CT%%20DE%%20DC%%20FL%%20GA%%20GU%%20HI%%20ID%%20IL%%20IN%%20IA%%20KS%%20KY%%20LA%%20ME%%20MD%%20MH%%20MA%%20MI%%20FM%%20MN%%20MS%%20MO%%20MT%%20NE%%20NV%%20NH%%20NJ%%20NM%%20NY%%20NC%%20ND%%20MP%%20OH%%20OK%%20OR%%20PW%%20PA%%20PR%%20RI%%20SC%%20SD%%20TN%%20TX%%20UT%%20VT%%20VA%%20VI%%20WA%%20WV%%20WI%%20WY'
        #creating HTTP Req
        req = urllib2.Request(url, data % locals())
        f = urllib2.urlopen(req)
    else:
        if debug:
            print "found %s" % filename
        f = open(filename)


    # create a subclass and override the handler methods
    class MyHTMLParser(HTMLParser):
        ratedEvents = []
        pendingEvent = None
        inTable = False
        lastTag = None

        def handle_starttag(self, tag, attrs):
            self.lastTag = tag
            if tag == 'table':
                self.inTable = True
            if tag == 'tr':
                self.pendingEvent = []
        def handle_endtag(self, tag):
            if tag == 'table':
                self.inTable = False
            if tag == 'tr':
                if len(self.pendingEvent) == 6:
                    self.ratedEvents.append(self.pendingEvent)
        def handle_data(self, data):
            if self.lastTag == 'td':
                self.pendingEvent.append(data)
    parser = MyHTMLParser()
    parser.feed(f.read())
    #for event in parser.ratedEvents:
    #    for subevent in event:
    #        print '%5s' % len(subevent), subevent
    return parser.ratedEvents
