#!/usr/bin/python3

import argparse
import csv
import os
import sqlite3

parser = argparse.ArgumentParser(description="""
        Liest Abkürzungslisten und schreibt sie in die Datenbank
        """)
parser.add_argument('--purge',
                    dest='purge',
                    help='Lösche erst alle alten Daten',
                    required=False,
                    action='store_true',
                    default=False)
args = parser.parse_args()

sql = sqlite3.connect('info.db')
sqlcursor = sql.cursor()
if args.purge:
    print("Purging old data...")
    sqlcursor.execute("""
        DELETE FROM shortstore
    """)

directory = 'data_sources'
for f in os.listdir(directory):
    if f[-4:] != '.csv':
        continue
    quelle = f[:-4]
    print("Processing source", quelle)
    with open('{}/{}'.format(directory, f)) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for datum in reader:
            abk = ' '.join(datum['Abk'].split())
            name = ' '.join(datum['Name'].split()).replace('.', '\u2024')
            kurzname = ' '.join(datum['Kurzname'].split())
            sqlcursor.execute("""
                REPLACE INTO
                    shortstore(
                        Abk,
                        Name,
                        Kurzname,
                        gueltigvon,
                        source
                    )
                    VALUES
                    (?,?,?,?,?)
                """,
                (abk
               , name
               , kurzname
               , datum['gültig von']
               , quelle
               , )
            )
sqlcursor.close()
sql.commit()
sql.close()
