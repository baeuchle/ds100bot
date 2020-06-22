#!/usr/bin/python3

'''Helper for tweeting bot statistics'''

import argparse
import datetime
from Externals import get_externals
import Mock
import Persistence.log as log

one_day = datetime.timedelta(days=1)
today = datetime.date.today()
first = today.replace(day=1)
january_first = first.replace(month=1)
first_last_month = (first - one_day).strftime("%Y%m01")
first_last_year = (january_first - one_day).strftime("%Y0101")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--readwrite',
                    dest='twmode',
                    help='Actually send tweets',
                    required=False,
                    action='store_const',
                    const='readwrite',
                    default='none')
parser.add_argument('--verbose', '-v',
                    dest='verbose',
                    help='Output lots of stuff',
                    required=False,
                    action='count')
parser.add_argument('--since',
                    dest='since',
                    help='Time frame for statistics',
                    required=False,
                    default=0)
args = parser.parse_args()

if args.verbose is None:
    args.verbose = 1
loglvl = 50 - args.verbose * 10
if loglvl <= 0:
    loglvl = 1

log.basicConfig(level=loglvl, style='{')
log_ = log.getLogger('statistics')

since = None
since_text = None
if args.since == 0 or args.since == "0":
    since = 0
    since_text = 'Beginn'
elif args.since == 'month':
    since = first_last_month
    since_text = 'Anfang letzten Monats'
elif args.since == 'year':
    since = first_last_year
    since_text = 'Anfang letzten Jahres'
else:
    since = int(args.since)
    since_text = since

api = get_externals(twmode=args.twmode, dbmode='readonly')
twapi = api.twitter
if twapi is None:
    twapi = Mock.MockApi()
# setup database
sql = api.database

counts = sql.count_status(since=since)
text = """Zeit für Statistik! Daten für die Zeit seit {}. Ich habe:
• {} Kürzel beantwortet, für
• {} Kürzel keine lange Version erkannt und
• {} nicht beantwortet, weil sie auf der Blacklist standen.

Die populärsten Kürzel waren:
""".format(
    since_text,
    counts.get('found', 0),
    counts.get('notfound', 0),
    counts.get('blacklist', 0)
)

for row in sql.popular_abbrs(since):
    text += "• {} ({}×)\n\u200b".format(row['S'], row['C'])
text += """
Die populärsten Quellen waren:
"""
for row in sql.popular_sources(since):
    text += "• {} ({}×)\n\u200b".format(row['S'], row['C'])
text += """
(Keine Garantie für richtiges Zählen)"""

twapi.tweet(text)
