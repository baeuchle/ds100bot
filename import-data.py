#!/usr/bin/python3

import argparse
import csv
from datetime import date
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

today = date.today().strftime("%Y%m%d")
directory = 'data_sources'
for f in os.listdir(directory):
    if f[-4:] != '.csv':
        continue
    quelle = f[:-4]
    print("Processing source", quelle)
    with open('{}/{}'.format(directory, f)) as csvfile:
        sqlcursor.execute("""
            SELECT
                abk_col,
                name_col,
                kurz_col,
                valid_from_col,
                valid_until_col,
                replace_links,
                delimiter
            FROM
                sources
            WHERE
                source_name = ?
        """,
            (quelle, )
        )
        headers = sqlcursor.fetchone()
        if headers == None:
            headers = ['Abk', 'Name', None, 'valid_from', 'valid_until', 1, ';']
        print(headers)
        reader = csv.DictReader(csvfile, delimiter=headers[6])
        for datum in reader:
            abk = ' '.join(datum[headers[0]].split())
            name = ' '.join(datum[headers[1]].split())
            kurzname = ''
            if headers[2] != None:
                kurzname = ' '.join(datum[headers[2]].split())
            valid_from = '00000000'
            valid_until = '99999999'
            if headers[3] != None:
                valid_from = datum[headers[3]]
                if valid_from > today:
                    continue
            if headers[4] != None:
                valid_until = datum[headers[4]]
                if valid_until < today:
                    continue
            if headers[5] == 1:
                name = name.replace('.', '\u2024')
            primkey = '{}::{}'.format(quelle, abk)
            sqlcursor.execute("""
                INSERT OR REPLACE
                INTO shortstore(
                    id,
                    Abk,
                    Name,
                    Kurzname,
                    gueltigvon,
                    source
                )
                VALUES
                (?,?,?,?,?,?)
            """,
                 (primkey
                , abk
                , name
                , kurzname
                , valid_from
                , quelle
                , )
            )
sqlcursor.close()
sql.commit()
sql.close()
