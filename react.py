def process_commands(tweet, twapi, readwrite, verbose):
    author = tweet.author()
    if tweet.has_hashtag('folgenbitte', case_sensitive=False):
        is_followed = twapi.is_followed(author)
        if verbose > 0:
            print ("folgenbitte from @{}:".format(author.screen_name), end='')
            if is_followed:
                print (" already following")
            else:
                print (" not yet following")
        if readwrite and not is_followed:
            twapi.follow(id=author)
    if tweet.has_hashtag('entfolgen', case_sensitive=False):
        is_followed = twapi.is_followed(author)
        if verbose > 0:
            print ("entfolgen from @{}:".format(author.screen_name), end='')
            if is_followed:
                print(" still following so far")
            else:
                print(" not even following yet")
        if readwrite and is_followed:
            twapi.defollow(author)
