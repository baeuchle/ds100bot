def process_commands(tweet, api, readwrite):
    myself = api.me()
    for ht in tweet.entities['hashtags']:
        try:
            api.create_friendship(id=tweet.author.id)
            if ht['text'].lower() == 'folgenbitte':
                friendship = api.show_friendship(myself.id, target_id=tweet.author.id)
                if not friendship[0].following and readwrite:
                    print ("Following user @{}".format(tweet.author.screen_name))
                    api.create_friendship(id=tweet.author.id)
            if ht['text'].lower() == 'entfolgen':
                friendship = api.show_friendship(myself.id, target_id=tweet.author.id)
                if not friendship[0].following and readwrite:
                    print ("Defollow user".format(tweet.author.screen_name))
                    api.destroy_friendship(id=tweet.author.id)
        except tweepy.TweepError as twerror:
            print("Error {} (de-)following @{}: {}".format(twerror.api_code, tweet.author.screen_name, twerror.reason))
