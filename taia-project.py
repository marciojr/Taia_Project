import tweepy
import requests
import urllib.request
import json

consumer_key = 'g5OJlrv1w7MUx2IUFRaasGOnG'
consumer_secret = '35qZhmwtwr5dtYDlLm048UH69dMxSa6xy2euSVQxqgIWM0zV9q'
access_token = '702339948-oigkMkwk59DcO8WkObCZU3jqhAFqWJAWbxEfyNuF'
access_token_secret = 'OUHoXSMNJvWNQOq7PQCWbbzEYxCqhedRd4LQ25GXvoKW6'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
OUR_API_KEY = "AIzaSyCKw-_Yp-ZXg243XtmQAET1giLOCJaQ5Ho"



api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
ids = api.friends_ids()
urls = []

for friend in ids:
    statuses = api.user_timeline(id=friend, count=50)
    for status in statuses:
        if status.entities and status.entities['urls']:
            for url in status.entities['urls']:
            	if '/youtu.be/' in url['expanded_url'] or'/youtube.com/' in url['expanded_url']:
                   urls.append((url['expanded_url'], status.author.screen_name))
with open('urls.csv', 'w') as f:
    for url in urls:
        f.write(url[0] + ',' + url[1] + '\n')
    f.close()

channels = []

for url in urls:
	u = url[0]
	video_id= ""
	channel_id = ""
	spl = u.split('/')

	if "/channel/"in u:
		channel_id = spl[len(spl)-1]
		channels.append(channel_id)
	else :
		if "youtu.be" in u:
			video_id = spl[len(spl)-1]
		elif "youtube.com" in u:
			aux = spl[len(spl)-1].split('&')
			video_id = aux[0][8:]

		ax = video_id.split('?')
		video_id = ax[0]

		
		url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id="+video_id+"&key="+OUR_API_KEY

		feed = urllib.request.urlopen(url)
		feed = feed.read().decode('utf-8')
		feed_json = json.loads(feed)
		print (video_id)
		if feed_json['items']: 
			channel_id = feed_json['items'][0]['snippet']['channelId']
			channels.append(channel_id)

tuplas =[]
aux = []
for i in channels:
	
	if i not in aux:
		aux.append(i)
		t = (channels.count(i), i)
		tuplas.append(t)
		
tuplas = sorted(tuplas, key = lambda t: t[0])
with open('channel.txt', 'w') as f:
    for t in tuplas:
        f.write(str(t[0]) + ',' + t[1] + '\n')
    f.close()