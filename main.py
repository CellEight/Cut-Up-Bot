import numpy as np
import re
from PIL import Image
from PIL import ImageFile
import requests
from io import BytesIO

ImageFile.LOAD_TRUNCATED_IMAGES = True

def cutUp(text):
    print(text)
    text = re.sub("@Dionysusintent", "", text)
    text = re.sub('https://t.co/[^\s]*', "", text)
    text = re.sub("[&]", "and", text)
    text = re.sub("[^.\w]", " ", text)
    #text = re.sub("[a-z]* [sm]")
    print(text)
    text = re.sub("\.{1}", " ", text)
    print(text)
    words = text.split()
    #while True:
    np.random.shuffle(words)
        #if words[0] != ".":
        #    break
    cut_up = ''
    for word in words:
        if word == ".":
            cut_up += "."
        else:
            cut_up += " " + word
    cut_up = cut_up[1:]
    return cut_up

import tweepy
from twitter_keys import *
import os

def tweet_image(url, username, status_id, status_text):
    filename = 'temp.jpg'
    # send a get request
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        # read data from downloaded bytes and returns a PIL.Image.Image object
        i = Image.open(BytesIO(request.content))
        # Saves the image under the given filename
        i.save(filename)
        glitch(filename)
        # Update the authenticated user’s status
        api.update_with_media('scramble.png', status=cutUp(status_text), in_reply_to_status_id=status_id)
    else:
        print("unable to download image")

def glitch(filename):
    os.system("python jpglitch.py "+filename +" -o scramble.png")

#create an OAuthHandler instance
# Twitter requires all requests to use OAuth for authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_secret)

 #Construct the API instance
api = tweepy.API(auth) # create an API object
#create a class inherithing from the tweepy  StreamListener
class BotStreamer(tweepy.StreamListener):

    # Called when a new status arrives which is passed down from the on_data method of the StreamListener
    def on_status(self, status):
        username = status.user.screen_name
        status_id = status.id
        status_text = status.text
        #print(username+" "+str(status_id)+": "+status_text)
        if 'media' in status.entities:
            for image in status.entities['media']:
                tweet_image(image['media_url'], username, status_id, status_text)
        else:
            api.update_status("@"+username+" "+cutUp(status_text))

myStreamListener = BotStreamer()

#Construct the Stream instance
stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['@Dionysusintent'])
