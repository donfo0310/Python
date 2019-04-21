import sys, csv
import tweepy

def GetTweet(screen_name, count):
    with open('api_setting/credentials.txt', mode='r') as f:
        consumer_key = f.readline().strip()
        consumer_secret = f.readline().strip()
        access_token_key = f.readline().strip()
        access_token_secret = f.readline().strip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)

    results = api.user_timeline(screen_name=screen_name, count=count)

    f = open('output.txt', 'w', encoding='UTF-8', newline='\n')
    writer = csv.writer(f)
    for result in results:
        writer.writerow([result.text.strip()])
    f.close()

if __name__ == '__main__':
    GetTweet(screen_name='duri0214', count=10)