import tweepy

import tweepy

import tweepy
import random
import requests
import urllib

username = 'toilet.io'
password = 'Toilettime'

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 \
    Safari/537.36'
#Fetch the available memes

data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
#List all the memes
ctr = 1
for img in images:
    print(ctr,img['name'])
    ctr = ctr+1


URL = 'https://api.imgflip.com/caption_image'


memes = [1,2,3,4,5,6,7,8,9,10]
id = random.choice(memes)
match id:
    case 1:
        text0 = name + " using excessive amounts of toilet paper"
        text1 = name + " using toilet paper in moderation"
    case 2:
        text0 = name + " using up " + number + " sheets of toilet paper"
        text1 = name + " planting " + str((int)number) + " trees instead"
    case 3:
        text0 = name + " being a friend to the environment"
        text1 = name + " using up " + str((int)number) + " sheets instead"
    case 4:
        text0 = name + " using " + str((int)number) + " sheets of toilet paper"
        text1 = name + " paying up " + price + " for next week's TP budget"
    case 5:
        text0 = name + " being a friend to the trees"
        text1 = name
params = {
    'username':username,
    'password':password,
    'template_id':images[id-1]['id'],
    'text0':"hello",
    'text1':"world"
}
response = requests.request('POST',URL,params=params).json()
url = response['data']['url']

client = tweepy.Client(consumer_key='NJR2pGSoieZyRk9jTPC4ypO9Z',
                        consumer_secret='L2GeDyGGzL0hezXQQJ5sF86g3nIlD7jg5DscebiSWgtd5ayC2N',
                        access_token='1496564796950519808-CNGNNX1gkZPSpqANxDUL73nFcrPkQM',
                        access_token_secret='vYFMKnfHdCFOGh8buoVtoNJ3Yw6oL9kOk7Gl09wThqiYa')

# # Replace the text with whatever you want to Tweet about
responses = client.create_tweet(text=url)
responses = client.create_tweet
print(responses)