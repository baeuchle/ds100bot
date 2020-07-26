"""Abstracts the abbreviation search result"""

import Persistence.log as log
log_ = log.getLogger(__name__)

class Result:
    # pylint: disable=R0902
    def __init__(self, candidate, db):
        self.candidate = candidate
        row = self.find_in_db(db.cursor)
        self.abbr = candidate.abbr
        if row is not None:
            self.long = row['name']
            self.status = row['status']
            self.source = row['req_xs']
            self.type = row['req_tc']
            self.default_source = row['def_xs']
            self.default_type = row['def_tc']
        else:
            self.long = ''
            self.status = 'notfound'
            self.source = ''
            self.type = candidate.type_character
            self.default_source = ''
            self.default_type = ''
        log_.debug("%s → %s", candidate, self)

    def __str__(self):
        if self.status == 'notfound':
            return 'None'
        return self.normalized() + '::' + self.long

    def normalized(self):
        if self.status == 'notfound':
            return None
        return '{}{}:{}'.format(self.type, self.source, self.abbr)

    def answered(self):
        text = '{}: {}\u200b\n'.format(self.abbr, self.long)
        if not (self.default_source == 'DS' or self.source == 'BOT'):
            text = '{}{}{}'.format(self.source, self.type, text)
        return text.replace('\\n', '\n')

    def find_in_db(self, sql):
        sql.execute("""
            SELECT
                shortstore.Abk as abk,
                shortstore.Name AS name,
                s1.explicit_source AS req_xs,
                s1.type AS req_tc,
                s2.explicit_source AS def_xs,
                s2.type AS def_tc,
                CASE
                    WHEN (
                        blacklist.Abk IS NOT NULL
                        AND
                        :explicit_source = ''
                    ) THEN 'blacklist'
                    ELSE 'found'
                END
                AS status
            FROM
                shortstore
            JOIN sources AS s1 ON s1.source_id = shortstore.source
            JOIN sources AS s2 ON s1.source_id = s2.source_id
            LEFT OUTER JOIN blacklist ON blacklist.Abk = shortstore.Abk
            WHERE
                shortstore.Abk = :abbr
            AND s1.type = :type_character
            AND (
                (:explicit_source != '' AND s1.explicit_source = :explicit_source)
                OR
                (:explicit_source == ''
                AND (s1.magic_hashtag = :magic_hashtag
                OR s1.explicit_source = 'BOT'
                )
                ))
            AND s2.is_default
            LIMIT 1
            """,
            self.candidate.get_dict()
        )
        return sql.fetchone()

    def loggable(self, magic_tags):
        if self.status in ('found', 'blacklist'):
            return True
        if self.candidate.explicit_source != '':
            return True
        if len(self.abbr) == 0 or len(self.abbr) > 5:
            return False
        if '#' + self.abbr in magic_tags:
            return False
        return True
