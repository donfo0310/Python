import  tweepy

def key_tweepy_proc():

    with open('api_setting/credentials.txt', mode='r') as f:
        consumer_key = f.readline().strip()
        consumer_secret = f.readline().strip()
        access_token_key = f.readline().strip()
        access_token_secret = f.readline().strip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth)

    return api