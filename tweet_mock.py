import copy
import re
from tweet import Tweet

import log
log_ = log.getLogger(__name__)

class User:
    def __init__(self, **kwargs):
        self.screen_name = kwargs['screen_name']
        self.id = kwargs['id']
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

User.theBot = User(
        id=1065715403622617089,
        id_str='1065715403622617089',
        name='DS100-Bot',
        screen_name='_ds_100',
        location='',
        description='Expandiert DS100-Abkürzungen. #DS100 und #$KURZ verwenden, oder den Bot taggen. #folgenbitte und der Bot findet #$KURZ ohne Aufforderung. Siehe Webseite.',
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
        profile_image_url='http://pbs.twimg.com/profile_images/1140888262619385856/dODzmIW9_normal.png',
        profile_image_url_https='https://pbs.twimg.com/profile_images/1140888262619385856/dODzmIW9_normal.png',
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
User.followed = User(id=11, id_str='11', name='Followee account', screen_name='followee', description='Fake: This user is followed by the bot.', follows=True)
User.notfollowed = User(id=12, id_str='12', name='Some other Account', screen_name='someotheraccount', description='Fake: This user is not followed by the bot.', follows=False)
User.followers = []
for i in range(21,26):
    User.followers.append(User(id=i, name='Follower', screen_name='follower{}'.format(i), follows=True))
User.nonfollowers = []
for i in range(31,37):
    User.nonfollowers.append(User(id=i, name='Nonfollower', screen_name='otherone{}'.format(i), follows=False))

class TweepyMock:
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
        if 'quoted_status_id' in self.raw:
            self.quoted_status_id = self.raw['quoted_status_id']
        else:
            self.quoted_status_id = None
        self.in_reply_to_status_id = self.raw['in_reply_to_status_id']
        self.expected_answer = self.raw.get('expected_answer', None)
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
    # signatures bot*:
    #  tl/nl: in timeline / not in timeline
    #  ab/ns/xs/na: abbreviation present (#FF, $123) / no sigil (FF) / explicit source (#DS:FF) / no abbreviation present
    #  xm/im: explicit mention / implicit mention (@ outside display_text_range)
    #  mt/md/me: magic tag / default magic tag / else magic tag
    #  pr/rt/re: pure retweet / retweet=quote / reply
    #  fs/fe #folgenbitte / #entfolgen
    list_of_tweets = []
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet should never been seen nor processed by the Bot. bot%nl%na%101',
        expected_answer=None,
        id=101,
        user=User.notfollowed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet should appear in the Bot’s timeline, but should be ignored. bot%tl%na%102',
        id=102,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100, but no other tweet. bot%tl%xm%na%103',
        id=103,
        entities={'user_mentions': [User.theBot.mention(31)]},
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100, but no other tweet. bot%nl%xm%na%104',
        id=104,
        entities={'user_mentions': [User.theBot.mention(31)]},
        user=User.notfollowed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet includes magic hashtag #DS100, but no other tweet. bot%tl%md%na%105',
        id=105,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet includes magic hashtag #DB640, but no other tweet. bot%nl%mt%na%106',
        id=106,
        user=User.notfollowed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet is ignored because of #NOBOT #FF bot%tl%me%301',
        id=107,
        user=User.followed,
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet my own #FF bot%...%108',
        id=108,
        user=User.theBot
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet pure retweet #FF bot%tl%ab%pr%109',
        id=109,
        retweeted_status=True,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#entfolgen bot%tl%fe%151',
        id=151,
        user=User.followers[0]
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#entfolgen bot%nl%fe%152',
        id=152,
        user=User.followers[1]
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#entfolgen @_ds_100 bot%xm%fe%153',
        id=153,
        entities={'user_mentions': [User.theBot.mention(12)]},
        user=User.followers[2]
        )))
    User.followers[2].follow_after = False
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='@_ds_100 #entfolgen bot%im%fe%154',
        id=154,
        display_text_range=[10,52],
        entities={'user_mentions': [User.theBot.mention(0)]},
        user=User.followers[3]
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#DS100 #entfolgen bot%mt%fe%155',
        id=155,
        user=User.followers[4]
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#folgenbitte bot%tl%fs%161',
        id=161,
        user=User.nonfollowers[0]
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#folgenbitte bot%nl%fs%162',
        id=162,
        user=User.nonfollowers[1]
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#folgenbitte @_ds_100 bot%xm%fs%163',
        id=163,
        entities={'user_mentions': [User.theBot.mention(12)]},
        user=User.nonfollowers[2]
        )))
    User.nonfollowers[2].follow_after = True
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='@_ds_100 #folgenbitte bot%im%fs%164',
        id=164,
        display_text_range=[10,62],
        entities={'user_mentions': [User.theBot.mention(0)]},
        user=User.nonfollowers[3]
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#DS100 #folgenbitte bot%mt%fs%165',
        id=165,
        entities={'user_mentions': []},
        user=User.nonfollowers[4]
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='@_ds_100 This tweet xm @_ds_100 in a reply #folgenbitte bot%nl%xm%im%fs%issue[9]%204',
        display_text_range=[9,75],
        id=166,
        entities={'user_mentions': [
            User.theBot.mention(0),
            User.theBot.mention(23)
        ]},
        user=User.nonfollowers[5]
        )))
    User.nonfollowers[5].follow_after = True
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet is quoted with explicit mention. bot%ns%nl%201 FF FK FM FW',
        expected_answer='FF: Frankfurt (Main) Hbf\nFK: Kassel Hbf\nFW: Wiesbaden Hbf',
        id=201,
        user=User.notfollowed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100 and quotes tweet bot%xm%rt[201]%221: https://t.co/f4k3url_12',
        expected_answer=None,
        id=221,
        entities={ 'user_mentions': [User.theBot.mention(31)] },
        user=User.notfollowed,
        quoted_status_id=201
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet is replied-to with explicit mention. bot%nl%ns%202 FF FK FM FW',
        expected_answer='FF: Frankfurt (Main) Hbf\nFK: Kassel Hbf\nFW: Wiesbaden Hbf',
        id=202,
        user=User.notfollowed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='@followee @_ds_100 This tweet: bot%xm%re[202]%222',
        id=222,
        entities={'user_mentions': [User.notfollowed.mention(0), User.theBot.mention(11)]},
        in_reply_to_status_id=202,
        in_reply_to_user_id=User.notfollowed.id,
        in_reply_to_screen_name=User.notfollowed.screen_name,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet is replied to with magic hashtag _FFM. bot%nl%ns%203 #FW',
        expected_answer='FFM#FW: Friedhof Westhausen',
        id=203,
        user=User.notfollowed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet replies with magic hashtag #_FFM. bot%nl%me%re[203]%223',
        id=223,
        user=User.notfollowed,
        in_reply_to_status_id=203,
        in_reply_to_user_id=User.notfollowed.id,
        in_reply_to_screen_name=User.notfollowed.screen_name
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='Hallo @_ds_100, do you know $1733? bot%tl%xm%ab[1,$]%issue[8]%301',
        expected_answer='1733: Hannover --Kassel-- - Würzburg',
        id=301,
        entities={'user_mentions': [ User.theBot.mention(6) ]},
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet plain tags #FF #_FH #DS:FFU #DS:_FKW #DS:HG_ bot%tl%ab%ns%401',
        expected_answer='FF: Frankfurt (Main) Hbf\nFFU: Fulda\nHG: Göttingen',
        id=401,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet different cases #DS:FF #DS:Fkw #ÖBB:Aa #ÖBB:AB bot%tl%xs%402',
        expected_answer='FF: Frankfurt (Main) Hbf\nÖBB#Aa: W․Mat․-Altmannsdorf (in Wbf)',
        id=402,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet blacklist #DBL #DS:WLAN bot%tl%bl%403',
        expected_answer='WLAN: Langen',
        id=403,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet mixes sources #MS #_FFM #WBC #_NO #OSL #DS:FF #BRG #DS100 #FKW bot%tl%ab%xs%is%mt%me%404',
        expected_answer='FFM#MS: Festhalle/Messe\nFFM#WBC: Willy-Brandt-Platz (C-Ebene)\nNO#OSL: Oslo S\nFF: Frankfurt (Main) Hbf\nNO#BRG: Bergen\nFKW: Kassel-Wilhelmshöhe',
        id=404,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet do not find CH = Chur #_CH #BS bot%tl%ab%mt%issue[13]%411',
        expected_answer='CH#BS: Basel SBB',
        id=411,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet make sure 411 works: #CH:CH bot%tl%xs%issue[13]%412',
        expected_answer='CH#CH: Chur',
        id=412,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅰ: #NO:249 #NO:ÅBY bot%tl%xs%unusual%420',
        expected_answer='NO#249: H-sign 249\nNO#ÅBY: Åneby',
        id=420,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅱ: $DS:VDE8¹ #CH:600133 #CH:ALT94 bot%tl%xs%unusual%421',
        expected_answer='VDE8¹: Nürnberg-Erfurt\nCH#600133: UNO Linie 600, km 133.179\nCH#ALT94: Altstätten SG 94',
        id=421,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅲ: #AT:Aa_G #AT:Aa_Z9 #AT:Z bot%tl%xs%unusual%422',
        expected_answer='AT#Aa G: Grenze ÖBB-WLB im km 7,610\nAT#Aa Z9: Wr․ Neudorf\nAT#Z: Zell am See',
        id=422,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅳ: #DS:AA_G #DS:AAG #DS:EM302 bot%tl%xs%unusual%423',
        expected_answer='AA G: Hamburg-Altona Gbf\nAAG: Ascheberg (Holst)\nEM302: Oberhausen Sbk M302',
        id=423,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅴ: #BOT:SARS_COV_2 #BOT:REKURSION #BOT:toggle bot%tl%xs%unusual%424',
        expected_answer='SARS COV 2: Dieser Bot ist offiziell Virusfrei™ und immun. Kuscheln, Händchenhalten etc. ist erlaubt. Bitte nicht anniesen (weil ist eklig).\nREKURSION: Siehe bitte #REKURSION',
        id=424,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅵ: #HH:HX #LP:K;#LP:KA+#LP:KALD bot%tl%xs%unusual%425',
        expected_answer='HH#HX: Hauptbahnhof-Nord\nLP#K: Köln Hbf\nLP#KA: Karlsruhe Hbf\nLP#KALD: Kaldenkirchen',
        id=425,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅶ: #UK:ABE #UK:ABER #NL:Ah;#NL:Ahg/#NL:Apn #NL:APD bot%tl%xs%unusual%426',
        expected_answer='UK#ABE: Aber\nUK#ABER: Aber\nNL#Ah: Arnhem\nNL#Ahg: Arnhem Goederenstation\nNL#Apn: Alphen aan den Rijn',
        id=426,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅷ: #FR:A?#FR:AA!#FR:AAA bot%tl%xs%unusual%427',
        expected_answer='FR#A: Angouleme\nFR#AA: Aire sur l\'Adour\nFR#AAA: Allassac',
        id=427,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅸ: $3640 #FFM:HB #FFM:_HB #FFM:211 #W:J $FFM:A3 bot%tl%xs%unusual%428',
        expected_answer='3640: Frankfurt-Höchst - Bad Soden\nFFM#HB: Frankfurt Hauptbahnhof\nFFM#_HB: WA Hauptbahnhof\nFFM#211: Hauptbahnhof\nW#J: Jedlersdorf (in F)\nFFM$A3: Anschlussstrecke A3: Abzweig Nordwest - Oberursel Hohemark',
        id=428,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol Ⅹ: $FFM:A $FFM:Aⅰ $FFM:AⅡ $FFM:AIII bot%tl%xs%unusual%429',
        expected_answer='FFM$A: A-Strecke: Südbahnhof - Heddernheim - (Ginnheim/Bad Homburg/Oberursel)\nFFM$Aⅰ: A-Strecke Teilabschnitt 1 Humser Straße - Hauptwache\nFFM$AⅡ: A-Strecke Teilabschnitt 2 Hauptwache - Willy-Brandt-Platz\nFFM$AIII: A-Strecke Teilabschnitt 3 Humser Straße - Weißer Stein',
        id=429,
        user=User.followed
        )))

    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅰ: #_NO #249 #ÅBY bot%tl%mt%unusual%430',
        expected_answer='NO#249: H-sign 249\nNO#ÅBY: Åneby',
        id=430,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅱ: #DS100 $VDE8¹ #_CH #600133 #ALT94 bot%tl%mt%unusual%431',
        expected_answer='VDE8¹: Nürnberg-Erfurt\nCH#600133: UNO Linie 600, km 133.179\nCH#ALT94: Altstätten SG 94',
        id=431,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅲ: #_AT #Aa_G #Aa_Z9 #_AT #Z bot%tl%mt%unusual%432',
        expected_answer='AT#Aa G: Grenze ÖBB-WLB im km 7,610\nAT#Aa Z9: Wr․ Neudorf\nAT#Z: Zell am See',
        id=432,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅳ: #_DS #AA_G #AAG #EM302 bot%tl%mt%unusual%433',
        expected_answer='AA G: Hamburg-Altona Gbf\nAAG: Ascheberg (Holst)\nEM302: Oberhausen Sbk M302',
        id=433,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅴ: #DS100 #SARS_COV_2 #REKURSION #toggle bot%tl%mt%unusual%434',
        expected_answer='SARS COV 2: Dieser Bot ist offiziell Virusfrei™ und immun. Kuscheln, Händchenhalten etc. ist erlaubt. Bitte nicht anniesen (weil ist eklig).\nREKURSION: Siehe bitte #REKURSION',
        id=434,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅵ: #_HH #HX #_LP #K;#KA+#KALD bot%tl%mt%unusual%435',
        expected_answer='HH#HX: Hauptbahnhof-Nord\nLP#K: Köln Hbf\nLP#KA: Karlsruhe Hbf\nLP#KALD: Kaldenkirchen',
        id=435,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅶ: #_UK #ABE #ABER #_NL #Ah;#Ahg/#Apn #APD bot%tl%mt%unusual%436',
        expected_answer='UK#ABE: Aber\nUK#ABER: Aber\nNL#Ah: Arnhem\nNL#Ahg: Arnhem Goederenstation\nNL#Apn: Alphen aan den Rijn',
        id=436,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅷ: #_FR #A?#AA!#AAA bot%tl%mt%unusual%437',
        expected_answer='FR#A: Angouleme\nFR#AA: Aire sur l\'Adour\nFR#AAA: Allassac',
        id=437,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅸ: #_DE $3640 #_FFM #HB #_HB #211 #_W #J #_FFM $A3 bot%tl%mt%unusual%438',
        expected_answer='3640: Frankfurt-Höchst - Bad Soden\nFFM#HB: Frankfurt Hauptbahnhof\nFFM#_HB: WA Hauptbahnhof\nFFM#211: Hauptbahnhof\nW#J: Jedlersdorf (in F)\nFFM$A3: Anschlussstrecke A3: Abzweig Nordwest - Oberursel Hohemark',
        id=438,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet unusual tags Vol ⅹ: #_FFM $A $Aⅰ $AⅡ $AIII bot%tl%mt%unusual%439',
        expected_answer='FFM$A: A-Strecke: Südbahnhof - Heddernheim - (Ginnheim/Bad Homburg/Oberursel)\nFFM$Aⅰ: A-Strecke Teilabschnitt 1 Humser Straße - Hauptwache\nFFM$AⅡ: A-Strecke Teilabschnitt 2 Hauptwache - Willy-Brandt-Platz\nFFM$AIII: A-Strecke Teilabschnitt 3 Humser Straße - Weißer Stein',
        id=439,
        user=User.followed
        )))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet media: #_FFM #HB #DS100 bot%tl%mt%mf%440',
        expected_answer='FFM#HB: Frankfurt Hauptbahnhof\nRALP: Alpirsbach\nHE: Emden\nMS: München Süd',
        extended_entities={'media': [ {'ext_alt_text': '#RALP' },
                                      {'ext_alt_text': '#_CH #HE' },
                                      {'ext_alt_text': '#MS' }
                                    ]},
        id=440,
        user=User.followed
        )))
    return list_of_tweets

def mocked_source():
    try:
        # pylint: disable=E0401,C0415
        from tweet_details import list_of_tweets
    except ModuleNotFoundError:
        log_.critical("Keine Tweet-Details gefunden. Bitte get_tweet.py mit --mode mock ausführen.")
    return list_of_tweets
