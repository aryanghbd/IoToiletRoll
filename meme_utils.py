from utils import *

#Global client in order to pass into functions.
username = 'toilet.io'
password = 'Toilettime'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 \
    Safari/537.36'

tweetclient = tweepy.Client(consumer_key='NJR2pGSoieZyRk9jTPC4ypO9Z',
                       consumer_secret='L2GeDyGGzL0hezXQQJ5sF86g3nIlD7jg5DscebiSWgtd5ayC2N',
                       access_token='1496564796950519808-CNGNNX1gkZPSpqANxDUL73nFcrPkQM',
                       access_token_secret='vYFMKnfHdCFOGh8buoVtoNJ3Yw6oL9kOk7Gl09wThqiYa')

def generate_meme_text(id, name, number):
    text0 = ''
    text1 = ''
    if id == 1:
            text0 = name + " using excessive amounts of toilet paper"
            text1 = name + " using toilet paper in moderation"
    if id == 2:
            text0 = name + " using up " + str((int)(number)) + " sheets of toilet paper"
            text1 = name + " planting " + str((int)(number)) + " trees instead"
    if id == 3:
            text0 = name + " being a friend to the environment"
            text1 = name + " using up " + str((int)(number)) + " sheets instead"
    if id == 4:
            text0 = name + " using " + str((int)(number)) + " sheets of toilet paper"
            text1 = name + " paying up for next week's TP budget"
    if id == 5:
            text0 = name + " being a friend to the trees"
            text1 = name
    return text0, text1

def generate_meme(name, number):
#Fetch the available memes
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
    #List all the memes
    URL = 'https://api.imgflip.com/caption_image'
    memes = [1,2,3,4,5]
    id = random.choice(memes)
    text0, text1 = generate_meme_text(id, name, number)
    params = {
        'username':username,
        'password':password,
        'template_id':images[id-1]['id'],
        'text0':text0,
        'text1':text1
    }
    response = requests.request('POST',URL,params=params).json()
    url = response['data']['url']


    # # Replace the text with whatever you want to Tweet about
    responses = tweetclient.create_tweet(text= "Looks like someone just used the loo and made a meme! " + url)
    responses = tweetclient.create_tweet
    print(responses)
    return 0