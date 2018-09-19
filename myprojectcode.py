#!/usr/bin/env python
# encoding: utf-8
# Author - Prateek Mehta


import tweepy  # https://github.com/tweepy/tweepy
import json
import wget
import urllib.request
import random
import string
import subprocess
from PIL import Image, ImageFont, ImageDraw
import os
import io
from google.cloud import vision
from google.cloud.vision import types
import sys


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


# Twitter API credentials
consumer_key = "S8LcuILJeofVWZkBilWkYrOYH"
consumer_secret = "he3oZTTPxDJG3XQdcWCRn16pSwEGfemX5grABi8NwF5LXC4Vbt"
access_key = "1039257149103394816-0nLYN7S16Ie1DflHcVgmotONLPmiBk"
access_secret = "LGikjWWaCVHQZ9SzBXRrEOlrE0lLfX2RiotNh5KDQuUIn"


def get_all_tweets(screen_name):
    """
    This function is used for using API to get tweets from twitter from a given user
    It will also generate two 'json' file, tweet.json is the whole content of tweet, and url.json is list of
    the whole media resources url.
    :param screen_name: known as username
    :return: all content in tweets, tweet_content is a 'List'
    """
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=20)
    # print(new_tweets)
    # print(type(new_tweets))
    # save most recent tweets
    alltweets.extend(new_tweets)
    # print(len(alltweets))
    # for i in alltweets:
    #     print(i.id)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    # print(oldest)

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=20, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)
        # for p in alltweets:
        #     print(p.id)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if (len(alltweets) > 15):
            break
        print("...%s tweets downloaded so far" % (len(alltweets)))



    # write tweet objects to JSON
    file = open('tweet.json', 'w')
    print("Writing tweet objects to JSON please wait...")
    # print(type(alltweets))
    for status in alltweets:
        json.dump(status._json, file, sort_keys=True, indent=4)

    # close the file
    print("Done")
    file.close()
    return alltweets



# if __name__ == '__main__':
#     # pass in the username of the account you want to download
# get_all_tweets("@ZhongyuanCai")


def get_media_url(alltweets):
    media_files = list()
    for status in alltweets:
        media = status.extended_entities.get('media')
        leng = len(media)
        if (len(media) > 0):
            for i in range(leng):
                media_files.append(media[i]['media_url'])

    # print(media_files)
    # print(len(media_files))
    filefile = open('url.json', 'w')
    print("writing url to Json, please wait...")
    json.dump(media_files, filefile)
    print("done")
    filefile.close()
    return media_files


def download_media(media_files):
    location = "./images/"
    i = 1
    leng = len(media_files)
    for res in media_files:
        name = "image" + str(i) + ".jpg"
        urllib.request.urlretrieve(res, location + name)
        print("downloading Numb.", i, '/', leng)
        i += 1
    print("finishing download")


def generate_video():
    print("start generating video")
    subprocess.call('ffmpeg -f image2 -framerate 1/5 -y -i ./images/image%d.jpg -c:v libx264 -pix_fmt yuv420p out.mp4', shell=True)
    print("video is done")
    pass


def resize_image(cd, width, height):
    direction = os.getcwd()
    os.chdir(cd)
    for root, dirs, files in os.walk("."):
        for filename in files:
            im1 = Image.open(filename)
            im1 = im1.resize((width, height), Image.ANTIALIAS)  # best down-sizing filter
            im1.save(filename)
            print(filename, "modification done")
    os.chdir(direction)


def get_label(cd):
    client = vision.ImageAnnotatorClient()
    label_all = []
    direction = os.getcwd()
    os.chdir(cd)
    for root, dirs, files in os.walk("."):
        for filename in files:
            print("getting label for", filename)
            file_name = os.path.join(
                os.path.dirname(__file__),
                filename)
            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)
            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations
            lab = []

            for label in labels:
                lab.append(label.description)
            label_all.append(lab)
    os.chdir(direction)
    return label_all


def add_label(cd, label, fontsize, num):
    from PIL import Image, ImageDraw, ImageFont, ImageColor
    # name = './imagetest/image1.jpg'
    direction = os.getcwd()
    os.chdir(cd)
    my_front = ImageFont.truetype("timesbd.ttf", size=fontsize)  # 50
    i = 0
    for root, dirs, files in os.walk("."):
        for filename in files:
            img = Image.open(filename)
            print("adding label to", filename)
            d = ImageDraw.Draw(img)

            if num > len(label):
                num = len(label)
            else:
                pass

            for j in range(num):
                d.text((10, 10 + j * fontsize), label[i][j], fill=(255, 0, 0), font=my_front)  # recommand j=3
                pass

            img.save(filename)
            i += 1
    os.chdir(direction)
    pass


twitter_content = get_all_tweets("@ZhongyuanCai")
url = get_media_url(twitter_content)
download_media(url)
resize_image("./images/", 1024, 768)
label = get_label("./images")
add_label("./images", label, 50, 3)
generate_video()
