import datetime
import copy
from tweet import Tweet

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
for i in range(31,36):
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
        self.entities = self.raw['entities']
        self.author = self.raw['user']
        self.display_text_range = self.raw['display_text_range']
        if 'quoted_status_id' in self.raw:
            self.quoted_status_id = self.raw['quoted_status_id']
        else:
            self.quoted_status_id = None
        self.in_reply_to_status_id = self.raw['in_reply_to_status_id']
        self.expected_answer = self.raw.get('expected_answer', None)

    def add_to_raw(self, key, val):
        if key not in self.raw:
            self.raw[key] = val


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

def mocked_tweets(verbose):
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
        entities={'hashtags': [], 'user_mentions': []},
        user=User.notfollowed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet should appear in the Bot’s timeline, but should be ignored. bot%tl%na%102',
        id=102,
        entities={'hashtags': [], 'user_mentions': []},
        user=User.followed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100, but no other tweet. bot%tl%xm%na%103',
        id=103,
        entities={'hashtags': [], 'user_mentions': [User.theBot.mention(31)]},
        user=User.followed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100, but no other tweet. bot%nl%xm%na%104',
        id=104,
        entities={'hashtags': [], 'user_mentions': [User.theBot.mention(31)]},
        user=User.notfollowed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet includes magic hashtag #DS100, but no other tweet. bot%tl%md%na%105',
        id=105,
        entities={'hashtags': [{'text': 'DS100', 'indices': [35, 40]}], 'user_mentions': []},
        user=User.followed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet includes magic hashtag #DB640, but no other tweet. bot%nl%mt%na%106',
        id=106,
        entities={'hashtags': [{'text': 'DB640', 'indices': [35, 40]}], 'user_mentions': []},
        user=User.notfollowed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#entfolgen bot%tl%fe%151',
        id=151,
        entities={'hashtags': [{'text': 'entfolgen', 'indices': [1, 10]}], 'user_mentions': []},
        user=User.followers[0]
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#entfolgen bot%nl%fe%152',
        id=152,
        entities={'hashtags': [{'text': 'entfolgen', 'indices': [1, 10]}], 'user_mentions': []},
        user=User.followers[1]
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#entfolgen @_ds_100 bot%xm%fe%153',
        id=153,
        entities={'hashtags': [{'text': 'entfolgen', 'indices': [1, 10]}], 'user_mentions': [User.theBot.mention(12)]},
        user=User.followers[2]
        ), verbose))
    User.followers[2].follow_after = False
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='@_ds_100 #entfolgen bot%im%fe%154',
        id=154,
        display_text_range=[10,52],
        entities={'hashtags': [{'text': 'entfolgen', 'indices': [11, 20]}], 'user_mentions': [User.theBot.mention(0)]},
        user=User.followers[3]
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#DS100 #entfolgen bot%mt%fe%155',
        id=155,
        entities={'hashtags': [{'text': 'DS100', 'indices': [1,8] }, {'text': 'entfolgen', 'indices': [11, 20]}], 'user_mentions': []},
        user=User.followers[4]
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#folgenbitte bot%tl%fs%161',
        id=161,
        entities={'hashtags': [{'text': 'folgenbitte', 'indices': [1, 12]}], 'user_mentions': []},
        user=User.nonfollowers[0]
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#folgenbitte bot%nl%fs%162',
        id=162,
        entities={'hashtags': [{'text': 'folgenbitte', 'indices': [1, 12]}], 'user_mentions': []},
        user=User.nonfollowers[1]
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#folgenbitte @_ds_100 bot%xm%fs%163',
        id=163,
        entities={'hashtags': [{'text': 'folgenbitte', 'indices': [1, 12]}], 'user_mentions': [User.theBot.mention(12)]},
        user=User.nonfollowers[2]
        ), verbose))
    User.nonfollowers[2].follow_after = True
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='@_ds_100 #folgenbitte bot%im%fs%164',
        id=164,
        display_text_range=[10,62],
        entities={'hashtags': [{'text': 'folgenbitte', 'indices': [11, 22]}], 'user_mentions': [User.theBot.mention(0)]},
        user=User.nonfollowers[3]
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='#DS100 #folgenbitte bot%mt%fs%165',
        id=165,
        entities={'hashtags': [{'text': 'DS100', 'indices': [1,8] }, {'text': 'folgenbitte', 'indices': [11, 22]}], 'user_mentions': []},
        user=User.nonfollowers[4]
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet is quoted with explicit mention. bot%ns%nl%201 FF FK FM FW',
        expected_answer='FF: Frankfurt (Main) Hbf\nFK: Kassel Hbf\nFW: Wiesbaden Hbf',
        id=201,
        entities={'hashtags': [], 'user_mentions': []},
        user=User.notfollowed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet explicitly mentions @_ds_100 and quotes tweet bot%xm%rt[201]%221: https://t.co/f4k3url_12',
        expected_answer=None,
        id=221,
        entities={'hashtags': [],
                  'user_mentions': [User.theBot.mention(31)]
                  },
        user=User.notfollowed,
        quoted_status_id=201
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet is replied-to with explicit mention. bot%nl%ns%202 FF FK FM FW',
        expected_answer='FF: Frankfurt (Main) Hbf\nFK: Kassel Hbf\nFW: Wiesbaden Hbf',
        id=202,
        entities={'hashtags': [], 'user_mentions': []},
        user=User.notfollowed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='@followee @_ds_100 This tweet: bot%xm%re[202]%222',
        id=222,
        entities={'hashtags': [], 'user_mentions': [User.notfollowed.mention(0), User.theBot.mention(11)]},
        in_reply_to_status_id=202,
        in_reply_to_user_id=User.notfollowed.id,
        in_reply_to_screen_name=User.notfollowed.screen_name,
        user=User.followed
        ), verbose))

    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet is replied to with magic hashtag _FFM. bot%nl%ns%203 #FW',
        expected_answer='FFM#FW Friedhof Westhausen',
        id=203,
        entities={'hashtags': [], 'user_mentions': []},
        user=User.notfollowed
        ), verbose))
    list_of_tweets.append(Tweet(TweepyMock(
        full_text='This tweet replies with magic hashtag #_FFM. bot%nl%me%re[203]%223',
        id=223,
        entities={'hashtags': [{'text': '_FFM', 'indices':[39,43]}], 'user_mentions': []},
        user=User.notfollowed,
        in_reply_to_status_id=203,
        in_reply_to_user_id=User.notfollowed.id,
        in_reply_to_screen_name=User.notfollowed.screen_name
        ), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1146760076478308352,
#         full_text='@followee FF: Frankfurt (Main) Hbf',
#         display_text_range=[10, 34],
#         entities={'hashtags': [], 'user_mentions': [User.followed.mention(0,0)]},
#         in_reply_to_status_id=1146759555579355141,
#         in_reply_to_user_id=11,
#         in_reply_to_screen_name='followee',
#         author=User.theBot,
#         user=User.theBot,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=1,
#         favorited=False,
#         retweeted=False,
#         lang='de'), verbose))
#     # list_of_tweets.append(Tweet(TweepyMock(
#     #     id=1146759675398041601,
#     #     full_text='Beispielretweet an @_ds_100 https://t.co/f4k3url_12',
#     #     display_text_range=[0, 27],
#     #     entities={'hashtags': [], 'user_mentions': [User.theBot.mention(0,0)]},
#     #     in_reply_to_status_id=None,
#     #     in_reply_to_user_id=None,
#     #     in_reply_to_screen_name=None,
#     #     author=User.followed,
#     #     user=User.followed,
#     #     geo=None,
#     #     coordinates=None,
#     #     place=None,
#     #     contributors=None,
#     #     quoted_status_id=1146759555579355141,
#     #     quoted_status_permalink={'url': 'https://t.co/f4k3url_12', 'expanded': 'https://twitter.com/followee/status/1146759555579355141', 'display': 'twitter.com/followee/statu…'},
#     #     quoted_status={'created_at': 'Thu Jul 04 12:35:58 +0000 2019', 'id': 1146759555579355141, 'id_str': '1146759555579355141', 'full_text': 'Beispieltweet zum einfacher Programmieren. FF', ''display_text_range': [0, 45], 'entities': {'hashtags': [], 'user_mentions': []}, 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 11, 'id_str': '11', 'name': 'Bjørn Bäuchle', 'screen_name': 'followee', 'location': '', 'description': 'Programmieren, Grün, Bahn, Norwegen, Physik, Gitarre. Kassel, Frankfurt, Göttingen. Linksgrünversifft, er/he/han.\nErsteller von @_ds_100.', 'url': 'https://t.co/f4k3url_12', 'entities': {'url': {}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 211, 'friends_count': 276, 'listed_count': 11, 'created_at': 'Tue Jan 18 21:27:31 +0000 2011', 'favourites_count': 2, 'utc_offset': None, 'time_zone': None, 'geo_enabled': False, 'verified': False, 'statuses_count': 6729, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': True, 'profile_background_color': '1BB00E', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/758220660825026560/hXxMnmts_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/758220660825026560/hXxMnmts_normal.jpg', 'profile_link_color': '1FA12D', 'profile_sidebar_border_color': '14751A', 'profile_sidebar_fill_color': '68ED71', 'profile_text_color': '8C9926', 'profile_use_background_image': False, 'has_extended_profile': False, 'default_profile': False, 'default_profile_image': False, 'following': True, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 0, 'favorite_count': 1, 'favorited': False, 'retweeted': False, 'lang': 'de'},
#     #     retweet_count=0,
#     #     favorite_count=0,
#     #     favorited=False,
#     #     retweeted=False,
#     #     possibly_sensitive=False,
#     #     lang='en'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1146759555579355141,
#         full_text='Beispieltweet zum einfacher Programmieren. #FW',
#         display_text_range=[0, 45],
#         entities={'hashtags': [], 'user_mentions': []},
#         in_reply_to_status_id=None,
#         in_reply_to_user_id=None,
#         in_reply_to_screen_name=None,
#         author=User.followed,
#         user=User.followed,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=1,
#         favorited=False,
#         retweeted=False,
#         lang='de'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1146759312066392064,
#         full_text='@_ds_100 Und darauf noch eine Beispielantwort. #FFBS',
#         display_text_range=[9, 52],
#         entities={'hashtags': [{'text': 'FFBS', 'indices': [47, 52]}], 'user_mentions': [User.theBot.mention(0,0)]},
#         in_reply_to_status_id=1146759071560847360,
#         in_reply_to_user_id=1065715403622617089,
#         in_reply_to_screen_name='_ds_100',
#         author=User.followed,
#         user=User.followed,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=0,
#         favorited=False,
#         retweeted=False,
#         lang='de'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1146759071560847360,
#         full_text='@followee FF: Frankfurt (Main) Hbf',
#         display_text_range=[10, 34],
#         entities={'hashtags': [], 'user_mentions': [User.followed.mention(0,0)]},
#         in_reply_to_status_id=1146758717154746370,
#         in_reply_to_user_id=11,
#         in_reply_to_screen_name='followee',
#         author=User.theBot,
#         user=User.theBot,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=0,
#         favorited=False,
#         retweeted=False,
#         lang='de'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1146758834448490496,
#         full_text='Beispieltweet zum einfacher Programmieren. #FF @_ds_100',
#         display_text_range=[0, 55],
#         entities={
#                 'hashtags': [{
#                         'text': 'FF',
#                         'indices': [43, 46]
#                         }],
#                 'user_mentions': [User.theBot.mention(0,0)],
#         },
#         in_reply_to_status_id=None,
#         in_reply_to_user_id=None,
#         in_reply_to_screen_name=None,
#         author=User.followed,
#         user=User.followed,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=0,
#         favorited=False,
#         retweeted=False,
#         lang='de'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         full_text='Dieser Tweet wird zitiert mit #_FFM https://t.co/f4k3url_12',
#         id=1146759891937300483,
#         display_text_range=[0, 24],
#         entities={'hashtags': [{'text': '_FFM', 'indices': [18, 24]}], 'user_mentions': []},
#         metadata={'iso_language_code': 'de', 'result_type': 'recent'},
#         in_reply_to_status_id=None,
#         in_reply_to_user_id=None,
#         in_reply_to_screen_name=None,
#         author=User.followed,
#         user=User.followed,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         quoted_status_id=1146759555579355141,
#         quoted_status={'created_at': 'Thu Jul 04 12:35:58 +0000 2019', 'id': 1146759555579355141, 'id_str': '1146759555579355141', 'full_text': 'Beispieltweet zum einfacher Programmieren. FF', 'display_text_range': [0, 45], 'entities': {'hashtags': [], 'user_mentions': []}, 'metadata': {'iso_language_code': 'de', 'result_type': 'recent'}, 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 11, 'id_str': '11', 'name': 'Bjørn Bäuchle', 'screen_name': 'followee', 'location': '', 'description': 'Programmieren, Grün, Bahn, Norwegen, Physik, Gitarre. Kassel, Frankfurt, Göttingen. Linksgrünversifft, er/he/han.\nErsteller von @_ds_100.', 'url': 'https://t.co/f4k3url_12', 'entities': {'url': {}, 'description': {'urls': []}}, 'protected': False, 'followers_count': 211, 'friends_count': 276, 'listed_count': 11, 'created_at': 'Tue Jan 18 21:27:31 +0000 2011', 'favourites_count': 2, 'utc_offset': None, 'time_zone': None, 'geo_enabled': False, 'verified': False, 'statuses_count': 6729, 'lang': None, 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': True, 'profile_background_color': '1BB00E', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/758220660825026560/hXxMnmts_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/758220660825026560/hXxMnmts_normal.jpg', 'profile_link_color': '1FA12D', 'profile_sidebar_border_color': '14751A', 'profile_sidebar_fill_color': '68ED71', 'profile_text_color': '8C9926', 'profile_use_background_image': False, 'has_extended_profile': False, 'default_profile': False, 'default_profile_image': False, 'following': True, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 0, 'favorite_count': 1, 'favorited': False, 'retweeted': False, 'lang': 'de'},
#         retweet_count=0,
#         favorite_count=0,
#         favorited=False,
#         retweeted=False,
#         possibly_sensitive=False,
#         lang='de'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1146758776227336192,
#         full_text='Beispieltweet zum einfacher Programmieren. #FF #DS100 #FFM:BO #DS:WLAN #DBL #DS:FF',
#         display_text_range=[0, 82],
#         entities={'hashtags': [
#             {'text': 'FF', 'indices': [43, 46]},
#             {'text': 'DS100', 'indices': [47, 53]},
#             {'text': 'FFM', 'indices': [54, 58]},
#             {'text': 'DS', 'indices': [63, 66]},
#             {'text': 'DBL', 'indices': [71, 75]}
#         ], 'user_mentions': []},
#         metadata={'iso_language_code': 'de', 'result_type': 'recent'},
#         in_reply_to_status_id=None,
#         in_reply_to_user_id=None,
#         in_reply_to_screen_name=None,
#         author=User.followed,
#         user=User.followed,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=0,
#         favorited=False,
#         retweeted=False,
#         lang='de'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1156084922941136896,
#         full_text='Test\nFKNZH\n@_ds_100',
#         display_text_range=[0, 16],
#         entities={'hashtags': [], 'user_mentions': [User.theBot.mention(0,0)]},
#         in_reply_to_status_id=None,
#         in_reply_to_user_id=None,
#         in_reply_to_screen_name=None,
#         author=User.notfollowed,
#         user=User.notfollowed,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=0,
#         favorited=False,
#         retweeted=False,
#         lang='en'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1156084922941136897,
#         full_text='Text #FF #DS100 #FW #_FFM #BM #DB640 #W #DS100 #FFES',
#         display_text_range=[0, 52],
#         entities={'hashtags': [
#             {'text': 'DS100', 'indices': [9, 15]},
#             {'text': '_FFM', 'indices': [20, 25]},
#             {'text': 'DB640', 'indices': [30, 36]},
#             {'text': 'DS100', 'indices': [40, 46]}
#             # other hashtags without relevance here.
#         ], 'user_mentions': []},
#         in_reply_to_status_id=None,
#         in_reply_to_user_id=None,
#         in_reply_to_screen_name=None,
#         author=User.notfollowed,
#         user=User.notfollowed,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=0,
#         favorited=False,
#         retweeted=False,
#         lang='en'), verbose))
#     list_of_tweets.append(Tweet(TweepyMock(
#         id=1156084922941136898,
#         full_text='#FF starts at the beginning! #DS100 #FW #_FFM #BM #DB640 #W #DS100 #FFES',
#         display_text_range=[0, 72],
#         entities={'hashtags': [
#             {'text': 'DS100', 'indices': [29, 35]},
#             {'text': '_FFM', 'indices': [40, 45]},
#             {'text': 'DB640', 'indices': [50, 56]},
#             {'text': 'DS100', 'indices': [60, 66]}
#             # other hashtags without relevance here.
#         ], 'user_mentions': []},
#         in_reply_to_status_id=None,
#         in_reply_to_user_id=None,
#         in_reply_to_screen_name=None,
#         author=User.notfollowed,
#         user=User.notfollowed,
#         geo=None,
#         coordinates=None,
#         place=None,
#         contributors=None,
#         retweet_count=0,
#         favorite_count=0,
#         favorited=False,
#         retweeted=False,
#         lang='en'), verbose))
    return list_of_tweets
