# import tweepy
# from tweepy import OAuthHandler
# import json
#
# consumer_key = 'S8LcuILJeofVWZkBilWkYrOYH'
# consumer_secret = 'he3oZTTPxDJG3XQdcWCRn16pSwEGfemX5grABi8NwF5LXC4Vbt'
# access_token = '1039257149103394816-0nLYN7S16Ie1DflHcVgmotONLPmiBk'
# access_secret = 'LGikjWWaCVHQZ9SzBXRrEOlrE0lLfX2RiotNh5KDQuUIn'
#
#
# @classmethod
# def parse(cls, api, raw):
#     status = cls.first_parse(api, raw)
#     setattr(status, 'json', json.dumps(raw))
#     return status
#
#
# # Status() is the data model for a tweet
# tweepy.models.Status.first_parse = tweepy.models.Status.parse
# tweepy.models.Status.parse = parse
# # User() is the data model for a user profil
# tweepy.models.User.first_parse = tweepy.models.User.parse
# tweepy.models.User.parse = parse
# # You need to do it for all the models you need
#
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)
#
# api = tweepy.API(auth)

import random
import string
# def random_string(length):
#     return ''.join(random.choice(string.ascii_letters) for m in range(length))
#
# print (type(random_string(10)))
# print (random_string(5))

import subprocess
# subprocess.call('ffmpeg -f image2 -framerate 1/5 -y -i ./images/image%d.jpg scr.avi', shell=True)
import os
from PIL import Image
# # os.system('ffmpeg -f image2 -framerate 1/5 -i ./images/image%d.jpg scr.avi')
# os.chdir("./images")
# for root, dirs, files in os.walk("."):
#     for filename in files:
#         print(filename)

# def resize_image(cd, width, height):
#     os.chdir(cd)
#     for root, dirs, files in os.walk("."):
#         for filename in files:
#             im1 = Image.open(filename)
#             im1 = im1.resize((width, height), Image.ANTIALIAS)  # best down-sizing filter
#             im1.save(filename)
#             print(filename, "modification done")
#
# resize_image("./images/", 1024, 768)

subprocess.call('ffmpeg -f image2 -framerate 1/5 -y -i ./images/image%d.jpg -c:v libx264 -pix_fmt yuv420p scr.avi', shell=True)
