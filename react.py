import tweepy

def process_commands(tweet, api, readwrite, verbose):
    myself = api.me()
    for ht in tweet.entities['hashtags']:
        text = ht['text'].lower()
        try:
            if text == 'folgenbitte':
                friendship = api.show_friendship(myself.id, target_id=tweet.author.id)
                if verbose > 0:
                    print ("folgenbitte from @{}:".format(tweet.author.screen_name), end='')
                    if friendship[0].following:
                        print (" already following")
                    else:
                        print (" not yet following")
                if readwrite and not friendship[0].following:
                    api.create_friendship(id=tweet.author.id)
            if text == 'entfolgen':
                friendship = api.show_friendship(myself.id, target_id=tweet.author.id)
                if verbose > 0:
                    print ("entfolgen from @{}:".format(tweet.author.screen_name), end='')
                    if friendship[0].following:
                        print(" still following so far")
                    else:
                        print(" not even following yet")
                if readwrite and friendship[0].following:
                    api.destroy_friendship(id=tweet.author.id)
        except tweepy.RateLimitError as rateerror:
            print("Rate limit violated: {}".format(rateerror.reason))
        except tweepy.TweepError as twerror:
            print("Error {} (de-)following @{}: {}".format(twerror.api_code, tweet.author.screen_name, twerror.reason))
