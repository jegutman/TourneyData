
import sys, os, time

year = '2013'
month = '03'

import subprocess

HISTORY = [
    ('2010', '01'),
    ('2010', '02'),
    ('2010', '03'),
    ('2010', '04'),
    ('2010', '05'),
    ('2010', '06'),
    ('2010', '07'),
    ('2010', '08'),
    ('2010', '09'),
    ('2010', '10'),
    ('2010', '11'),
    ('2010', '12'),

    ('2011', '01'),
    ('2011', '02'),
    ('2011', '03'),
    ('2011', '04'),
    ('2011', '05'),
    ('2011', '06'),
    ('2011', '07'),
    ('2011', '08'),
    ('2011', '09'),
    ('2011', '10'),
    ('2011', '11'),
    ('2011', '12'),

    ('2012', '01'),
    ('2012', '02'),
    ('2012', '03'),
    ('2012', '04'),
    ('2012', '05'),
    ('2012', '06'),
    ('2012', '07'),
    ('2012', '08'),
    ('2012', '09'),
    ('2012', '10'),
    ('2012', '11'),
    ('2012', '12'),

    ('2013', '01'),
    ('2013', '02'),
    ('2013', '03'),
    ('2013', '04'),
    ('2013', '05'),
    ('2013', '06'),
    ('2013', '07'),
    ('2013', '08'),
    ('2013', '09'),
    ('2013', '10'),
]

from findHighestRated import *

for year, month in HISTORY:

    datePrefix = '%(year)s%(month)s' % locals()
    filename = '/tmp/ratedlist%(year)s%(month)s' % locals()

    try:
        data = open(filename)
    except:
        command = ['wget', 'http://www.uschess.org/datapage/events-rated.php', '--post-data', 'month=%(month)s/%(year)s&states=AL%%20AK%%20AS%%20AZ%%20AR%%20CA%%20CO%%20CT%%20DE%%20DC%%20FL%%20GA%%20GU%%20HI%%20ID%%20IL%%20IN%%20IA%%20KS%%20KY%%20LA%%20ME%%20MD%%20MH%%20MA%%20MI%%20FM%%20MN%%20MS%%20MO%%20MT%%20NE%%20NV%%20NH%%20NJ%%20NM%%20NY%%20NC%%20ND%%20MP%%20OH%%20OK%%20OR%%20PW%%20PA%%20PR%%20RI%%20SC%%20SD%%20TN%%20TX%%20UT%%20VT%%20VA%%20VI%%20WA%%20WV%%20WI%%20WY' % locals(), '-O', '%(filename)s' % locals()]
        subprocess.Popen(command)
        time.sleep(8)
        data = open(filename)
    for line in data:
        line = line.replace('\n', '')
        line = line.replace('&nbsp', '')
        line = line.replace(';', '')
        if datePrefix in line:
            for i in line.split('</tr>'):
                i = i.replace('<tr>', '')
                i = i.replace('<td>', '')
                
                i = [j for j in i.split('</td>') if j]
                if len(i) != 6:
                    continue
                i[0] = i[0].split('>')[1].split('<')[0]
                eventId, eventName, city, state, players, localPct = i
                print eventId
                #if city == 'AUSTIN' and state == 'TX':
                #    playerInfo = findHighestRated(eventId)
                #    print i, playerInfo
