# pylint: disable=C0114

import copy
import re

import logging
log_ = logging.getLogger(__name__)

class User:
    # pylint: disable=R0903
    def __init__(self, **kwargs):
        self.screen_name = kwargs['screen_name']
        self._name = kwargs['screen_name']
        self.id = kwargs['id']
        self._id = kwargs.get('id_str', str(self.id))
        self._mention = {
            'screen_name': self.screen_name,
            'name': kwargs['name'],
            'id': self.id,
            'indices': [0, 0]
        }
        self.follows = kwargs.get('follows', False)
        self.follow_after = self.follows

    def mention(self, start):
        result = copy.deepcopy(self._mention)
        result['indices'][0] = start
        result['indices'][1] = start + len(self.screen_name)
        return result

    def __str__(self):
        return self._name

User.theBot = User(
        id=1065715403622617089,
        id_str='1065715403622617089',
        name='DS100-Bot',
        screen_name='_ds_100',
        location='',
        description='''Expandiert DS100-Abkürzungen. #DS100 und #$KURZ verwenden, oder den Bot
        taggen. #folgenbitte und der Bot findet #$KURZ ohne Aufforderung. Siehe Webseite.''',
        url='https://t.co/s7A9JO049r',
        entities={
                'url': {
                        'urls': [{
                                'url': 'https://t.co/s7A9JO049r',
                                'expanded_url': 'https://ds100.frankfurtium.de/',
                                'display_url': 'ds100.frankfurtium.de',
                                'indices': [0, 23]
                                }]
                       },
                'description': {'urls': []}
        },
        protected=False,
        followers_count=61,
        friends_count=29,
        listed_count=0,
        favourites_count=0,
        utc_offset=None,
        time_zone=None,
        geo_enabled=False,
        verified=False,
        statuses_count=250,
        lang=None,
        contributors_enabled=False,
        is_translator=False,
        is_translation_enabled=False,
        profile_background_color='F5F8FA',
        profile_background_image_url=None,
        profile_background_image_url_https=None,
        profile_background_tile=False,
        profile_image_url=
            'http://pbs.twimg.com/profile_images/1140888262619385856/dODzmIW9_normal.png',
        profile_image_url_https=
            'https://pbs.twimg.com/profile_images/1140888262619385856/dODzmIW9_normal.png',
        profile_link_color='1DA1F2',
        profile_sidebar_border_color='C0DEED',
        profile_sidebar_fill_color='DDEEF6',
        profile_text_color='333333',
        profile_use_background_image=True,
        has_extended_profile=False,
        default_profile=True,
        default_profile_image=False,
        following=False,
        follow_request_sent=False,
        notifications=False,
        translator_type='none',
        follows=True)
User.followed = User(id=11, id_str='11',
                     name='Followee account',
                     screen_name='followee',
                     description='Fake: This user is followed by the bot.',
                     follows=True)
User.notfollowed = User(id=12, id_str='12',
                        name='Some other Account',
                        screen_name='someotheraccount',
                        description='Fake: This user is not followed by the bot.',
                        follows=False)

class TweepyMock:
    # pylint: disable=R0902
    def __init__(self, **kwargs):
        self.raw = kwargs
        self.add_to_raw('expected_answer', None)
        self.add_to_raw('display_text_range', [0, len(self.raw['full_text'])])
        self.add_to_raw('in_reply_to_status_id', None)
        self.add_to_raw('in_reply_to_user_id', None)
        self.add_to_raw('in_reply_to_screen_name', None)
        self.id = self.raw['id']
        self.full_text = self.raw['full_text']
        self.create_entities()
        self.author = self.raw['user']
        self.display_text_range = self.raw['display_text_range']
        self.quoted_status_id = kwargs.get('quoted_status_id', None)
        self.in_reply_to_status_id = self.raw['in_reply_to_status_id']
        self.expected_answer = self.raw.get('expected_answer', None)
        self.retweeted_status = self.raw.get('retweeted_status', False)
        if 'extended_entities' in self.raw:
            self.extended_entities = self.raw['extended_entities']

    def add_to_raw(self, key, val):
        if key not in self.raw:
            self.raw[key] = val

    def create_entities(self):
        self.add_to_raw('entities', {})
        if 'hashtags' not in self.raw['entities']:
            # create your own hashtag list
            ht = re.compile(r"""\#(\w+)""")
            self.raw['entities']['hashtags'] = []
            for t in ht.finditer(self.full_text):
                self.raw['entities']['hashtags'].append({
                    'text': t.group(1),
                    'indices': [t.start(1), t.end(1)]
                })
        if 'user_mentions' not in self.raw['entities']:
            self.raw['entities']['user_mentions'] = []
        self.entities = self.raw['entities']

    def __str__(self):
        lines = self.full_text.splitlines()
        length = max([len(l) for l in lines])
        length = max(length, len(self.author.screen_name) + 2)
        result = "┏{}┓\n".format('━'*(length+2))
        result += ("┃ @{{:{}}} ┃\n".format(length - 1)).format(self.author.screen_name + ":")
        for l in lines:
            result += ("┃ {{:{}}} ┃\n".format(length)).format(l)
        result += "┗{}┛".format('━'*(length+2))
        return result

def mocked_tweets():
    # pylint: disable=C0301, R0915
    # signatures bot*:
    #  tl/nl: in timeline / not in timeline
    #  ab/ns/xs/na: abbreviation present (#FF, $123) / no sigil (FF) / explicit source (#DS:FF) / no abbreviation present
    #  xm/im: explicit mention / implicit mention (@ outside display_text_range)
    #  mt/md/me: magic tag / default magic tag / else magic tag
    #  pr/rt/re: pure retweet / retweet=quote / reply
    #  fs/fe #folgenbitte / #entfolgen
    list_of_tweets = []
    list_of_tweets.append(TweepyMock(
        full_text='This tweet should never been seen nor processed by the Bot. bot%nl%na%101',
        expected_answer=None,
        id=101,
        user=User.notfollowed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet should appear in the Bot’s timeline, but should be ignored. bot%tl%na%102',
        id=102,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100, but no other tweet. bot%tl%xm%na%103',
        id=103,
        entities={'user_mentions': [User.theBot.mention(31)]},
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100, but no other tweet. bot%nl%xm%na%104',
        id=104,
        entities={'user_mentions': [User.theBot.mention(31)]},
        user=User.notfollowed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet includes magic hashtag #DS100, but no other tweet. bot%tl%md%na%105',
        id=105,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet includes magic hashtag #DB640, but no other tweet. bot%nl%mt%na%106',
        id=106,
        user=User.notfollowed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet is ignored because of #NOBOT #FF bot%tl%me%301',
        id=107,
        user=User.followed,
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet my own #FF bot%...%108',
        id=108,
        user=User.theBot
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet pure retweet #FF bot%tl%ab%pr%109',
        id=109,
        retweeted_status=True,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet is quoted with explicit mention. bot%ns%nl%201 FF FK FM FW',
        expected_answer='FF: Frankfurt (Main) Hbf\nFK: Kassel Hbf\nFW: Wiesbaden Hbf',
        id=201,
        user=User.notfollowed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100 and quotes tweet bot%xm%rt[201]%221: https://t.co/f4k3url_12',
        expected_answer=None,
        id=221,
        entities={'user_mentions': [User.theBot.mention(31)]},
        user=User.notfollowed,
        quoted_status_id=201
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet is replied-to with explicit mention. bot%nl%ns%202 FF FK FM FW',
        expected_answer='FF: Frankfurt (Main) Hbf\nFK: Kassel Hbf\nFW: Wiesbaden Hbf',
        id=202,
        user=User.notfollowed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='@followee @_ds_100 This tweet: bot%xm%re[202]%222',
        id=222,
        entities={'user_mentions': [User.notfollowed.mention(0), User.theBot.mention(11)]},
        in_reply_to_status_id=202,
        in_reply_to_user_id=User.notfollowed.id,
        in_reply_to_screen_name=User.notfollowed.screen_name,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet is replied to with magic hashtag _FFM. bot%nl%ns%203 #FW',
        expected_answer='FFM#FW: Friedhof Westhausen',
        id=203,
        user=User.notfollowed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet replies with magic hashtag #_FFM. bot%nl%me%re[203]%223',
        id=223,
        user=User.notfollowed,
        in_reply_to_status_id=203,
        in_reply_to_user_id=User.notfollowed.id,
        in_reply_to_screen_name=User.notfollowed.screen_name
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet my own will be quoted #FF bot%tl%ab%204',
        id=204,
        user=User.theBot
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet quotes myself, @_ds_100! bot%tl%ab%pr%re[204]%224',
        id=224,
        entities={'user_mentions': [User.theBot.mention(26)]},
        user=User.followed,
        in_reply_to_status_id=204,
        in_reply_to_screen_name=User.theBot.screen_name
        ))
    list_of_tweets.append(TweepyMock(
        full_text='Hallo @_ds_100, do you know $1733? bot%tl%xm%ab[1,$]%issue[8]%301',
        expected_answer='1733: Hannover --Kassel-- - Würzburg',
        id=301,
        entities={'user_mentions': [User.theBot.mention(6)]},
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet blacklist #DBL #DS:WLAN bot%tl%bl%403',
        expected_answer='WLAN: Langen',
        id=403,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet mixes sources #MS #_FFM #WBC #_NO #OSL #DS:FF #BRG #DS100 #FKW bot%tl%ab%xs%is%mt%me%404',
        expected_answer='FFM#MS: Festhalle/Messe\nFFM#WBC: Willy-Brandt-Platz (C-Ebene)\nNO#OSL: Oslo S\nFF: Frankfurt (Main) Hbf\nNO#BRG: Bergen\nFKW: Kassel-Wilhelmshöhe',
        id=404,
        user=User.followed
        ))

    # former testcases 430-439 repeat 420-429, now found in tests/test_find_tokens, only with magic
    # hashtags instead of explicit sources.
    list_of_tweets.append(TweepyMock(
        full_text='This tweet media: #_FFM #HB #DS100 bot%tl%mt%mf%440',
        expected_answer='FFM#HB: Frankfurt Hauptbahnhof\nRALP: Alpirsbach\nCH#HE: Herisau\nCH#MS: Münsingen',
        extended_entities={'media': [{'ext_alt_text': '#RALP'},
                                     {'ext_alt_text': '#_CH #HE'},
                                     {'ext_alt_text': '#MS'}
                                    ]},
        id=440,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet media w/o ext_alt: #_FFM #HB bot%tl%mt%mf%441',
        expected_answer='FFM#HB: Frankfurt Hauptbahnhof',
        extended_entities={'media': [{},
                                     {}
                                    ]},
        id=441,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='This tweet media w/o media: #_FFM #HB bot%tl%mt%mf%442',
        expected_answer='FFM#HB: Frankfurt Hauptbahnhof',
        extended_entities={},
        id=442,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='Blacklist #LZB &amp;LZB bot%tl%bl%451',
        expected_answer='LZB: Linienförmige Zugbeeinflussung',
        id=451,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='Repeated things #FF #FF bot%tl%460',
        expected_answer='FF: Frankfurt (Main) Hbf',
        id=460,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='Repeated things #_FFM #DS:FF #DS100 #DE:FF #FF bot%tl%461',
        expected_answer='FF: Frankfurt (Main) Hbf',
        id=461,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='Bot precedence #AI #_CH #BOT:AI bot%tl%462',
        expected_answer='CH#AI: Airolo\nAI: Dieser Bot besitzt keine Künstliche Intelligenz. Er ist sozusagen strunzdumm. Lernen kann der Bot nur, indem der Autor lernt und etwas neues dazuprogrammiert.',
        id=462,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='Bot precedence #CH:AI #AI bot%tl%463',
        expected_answer='CH#AI: Airolo\nAI: Dieser Bot besitzt keine Künstliche Intelligenz. Er ist sozusagen strunzdumm. Lernen kann der Bot nur, indem der Autor lernt und etwas neues dazuprogrammiert.',
        id=463,
        user=User.followed
        ))
    list_of_tweets.append(TweepyMock(
        full_text='Bot flag emoji \U0001F1E6\U0001F1F9 #FAQ:AUSLAND bot%tl%501',
        expected_answer=('FAQ#AUSLAND: Kürzel mit X und Z haben als zweiten Buchstaben das Land: '
            + 'XA\U0001F1E6\U0001F1F9 '
            + 'XB\U0001F1E7\U0001F1EA '
            + 'XC\U0001f1f7\U0001f1fa '
            + 'XD\U0001f1e9\U0001f1f0 '
            + 'XE\U0001f1ea\U0001f1f8 '
            + 'XF\U0001f1eb\U0001f1f7 '
            + 'XG\U0001f1ec\U0001f1f7 '
            + 'XH\U0001f1eb\U0001f1ee '
            + 'XI\U0001f1ee\U0001f1f9 '
            + 'XJ\U0001f1f7\U0001f1f8 '
            + 'XK\U0001f1ec\U0001f1e7 '
            + 'XL\U0001f1f1\U0001f1fa '
            + 'XM\U0001f1ed\U0001f1fa '
            + 'XN\U0001f1f3\U0001f1f1 '
            + 'XO\U0001f1f3\U0001f1f4 '
            + 'XP\U0001f1f5\U0001f1f1 '
            + 'XQ\U0001f1f9\U0001f1f7 '
            + 'XR\U0001f1ed\U0001f1f7 '
            + 'XS\U0001f1e8\U0001f1ed '
            + 'XT\U0001f1e8\U0001f1ff '
            + 'XU\U0001f1f7\U0001f1f4 '
            + 'XV\U0001f1f8\U0001f1ea '
            + 'XW\U0001f1e7\U0001f1ec '
            + 'XX\U0001f1f5\U0001f1f9 '
            + 'XY\U0001f1f8\U0001f1f0 '
            + 'XZ\U0001f1f8\U0001f1ee '
            + 'ZA\U0001f1f2\U0001f1f0 '
            + 'ZB\U0001f1e7\U0001f1e6 '
            + 'ZE\U0001f1ea\U0001f1ea '
            + 'ZI\U0001f1ee\U0001f1ea '
            + 'ZK\U0001f1f0\U0001f1ff '
            + 'ZL\U0001f1f1\U0001f1f9 '
            + 'ZM\U0001f1f2\U0001f1e9 '
            + 'ZT\U0001f1f1\U0001f1fb '
            + 'ZU\U0001f1fa\U0001f1e6 '
            + 'ZW\U0001f1e7\U0001f1fe'
        ),
        id=501,
        user=User.followed
        ))
    return list_of_tweets

def mocked_source():
    try:
        # pylint: disable=E0401,C0415
        from tweet_details import list_of_tweets
    except ModuleNotFoundError:
        log_.critical("Keine Tweet-Details gefunden. Bitte get_tweet mit --mode mock ausführen.")
        return []
    return list_of_tweets
