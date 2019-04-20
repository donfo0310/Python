import sys, csv
import tweepy

from key_tweepy import key_tweepy_proc

api = key_tweepy_proc()

results = api.user_timeline(screen_name="duri0214", count=10)

f = open('output.txt', 'w', encoding='UTF-8', newline='\n')
writer = csv.writer(f)

for result in results:
    writer.writerow([result.text.strip()])

f.close()