#!/usr/bin/python3

import api
from database import Database
import gitdescribe as git

import argparse
import sys
import datetime

one_day = datetime.timedelta(days=1)
today = datetime.date.today()
first = today.replace(day=1)
january_first = first.replace(month=1)
first_last_month = (first - one_day).strftime("%Y%m01")
first_last_year = (january_first - one_day).strftime("%Y0101")

parser = argparse.ArgumentParser(description='Helper for tweeting bot statistics')
parser.add_argument('--readwrite',
                    dest='rw',
                    help='Actually send tweets',
                    required=False,
                    action='store_true',
                    default=False)
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

api_name = 'mock'
if args.rw:
    api_name = 'readwrite'
if args.verbose is None:
    args.verbose = 1

since = None
since_text = None
print(args.since, args.since == 0)
if args.since == 0:
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

# setup twitter API
twapi = api.get_api_object(api_name, args.verbose, external=False)
# setup database
sql = Database('readonly', args.verbose)

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
    text += "• {} ({}×)\n​".format(row['S'], row['C'])
text += """
Die populärsten Quellen waren:
"""
for row in sql.popular_sources(since):
    text += "• {} ({}×)\n​".format(row['S'], row['C'])
text += """
(Keine Garantie für richtiges Zählen)"""

twapi.tweet(text)
sql.close_sucessfully()
