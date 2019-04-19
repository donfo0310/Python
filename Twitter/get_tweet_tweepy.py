import  sys
import  tweepy

from key_tweepy import key_tweepy_proc

api = key_tweepy_proc()

results = api.user_timeline(screen_name="duri0214", count=10)
#
for result in results:
    print(result.id)
    print(result.created_at)
    print(result.text)
    print()