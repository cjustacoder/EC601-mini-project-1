#!/usr/bin/env python
# encoding: utf-8

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
import datetime
import mysql.connector

def random_string(length):
    """
    generate a certain length of random string(was used for rename the images download)
    :param length: the length of random string
    :return: the random string
    """
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


def get_all_tweets(screen_name, filename):
    """
    This function is used for using API to get tweets from twitter from a given user.

    It will also generate two 'json' file, tweet.json is the whole content of tweet, and url.json is list of
    the whole media resources url. You need to uncomment the correspondent part to enable these function.
    part refer to tweetAPIexample from class
    :param screen_name: known as username
    :param filename: the file which you store your Twitter credential
    :return: all content in tweets, tweet_content is a 'List'
    """
    # Twitter authentication get
    authent = read_twit_cred(filename)
    consumer_key = authent[0]
    consumer_secret = authent[1]
    access_key = authent[2]
    access_secret = authent[3]
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=20)

    # save most recent tweets
    alltweets.extend(new_tweets)
    try:
    # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
    except:
        sys.stderr.write("Failed to acquire tweets or there is no tweets in this account \n")
        raise
    # print(oldest)

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=20, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if (len(alltweets) > 15):
            break
        print("...%s tweets downloaded so far" % (len(alltweets)))

    # uncomment the following lines if you need to write tweet objects to JSON
    # file = open('tweet.json', 'w')
    # print("Writing tweet objects to JSON please wait...")
    # # print(type(alltweets))
    # for status in alltweets:
    #     json.dump(status._json, file, sort_keys=True, indent=4)
    #
    # # close the file
    # print("Done")
    # file.close()
    return alltweets


def get_media_url(alltweets):
    """
    To extract medial url from given tweet content
    :param alltweets: given tweet content
    :return: a List of all media url in the content
    """
    media_files = list()
    try:
        for status in alltweets:
            media = status.extended_entities.get('media')
            leng = len(media)
            if (len(media) > 0):
                for i in range(leng):
                    media_files.append(media[i]['media_url'])
    except:
        sys.stderr.write("Failed to acquire media from tweets or there is no media in tweets\n")
        raise


    # uncomment the following lines if you need to print json file of url
    # filefile = open('url.json', 'w')
    # print("writing url to Json, please wait...")
    # json.dump(media_files, filefile)
    # print("done")
    # filefile.close()
    return media_files


def download_media(media_files, number, limit):
    """
    To down load the media files from given media url,
    then store all these files into "./images" folder
    :param media_files: given media url
    :param number: given the number of media you want
    :param number: limitation of number of images
    :return: None
    """
    location = "./images/"
    i = 1
    leng = len(media_files)
    if leng > number:
        leng = number
    else:
        print("number of image beyond the content, download whole images\nnumber is ", leng)
        pass
    if leng > limit:
        leng = limit
        number = limit
    for res in media_files:
        name = "image" + str(i) + ".jpg"
        urllib.request.urlretrieve(res, location + name)
        print("downloading Numb.", i, '/', leng)
        i += 1
        if (i > number):
            break

    print("finishing download")


def generate_video(framerate, cd, outcome):
    """
    generate video with ffmpeg with certain parameters
    :param framerate: assign the frame rate of video
    :param cd: assign the content source direction to make video
    :param outcome: assign the name and format of video
    :return: None
    """
    print("start generating video")
    subprocess.call('ffmpeg -f image2 -framerate ' + framerate +
                    ' -y -i ' + cd + ' -c:v libx264 -pix_fmt yuv420p ' + outcome, shell=True)
    print("video is done")
    pass


def resize_image(cd, width, height):
    """
    resize all the image down loaded to a uniform size to avoid difficulties in generating video
    :param cd: the location of images
    :param width: assign the width of size
    :param height: assign the height of size
    :return: None
    """
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
    """
    use google vision to get descriptions of images
    :param cd: the direction where images are stored
    :return: a two array List of labels of all images
    """
    try:
        client = vision.ImageAnnotatorClient()
    except:
        sys.stderr.write('Some thing is wrong with Google Auth\n')
        raise
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
            try:
                response = client.label_detection(image=image)
            except:
                sys.stderr.write("Something is wrong with Google Vision API\n")
                raise
            labels = response.label_annotations
            lab = []

            for label in labels:
                lab.append(label.description)
            label_all.append(lab)
    os.chdir(direction)
    return label_all


def add_label(cd, label, fontsize, num):
    """
    draw labels on the corresponding image
    :param cd: the direction where images are stored
    :param label: the label acquired from google vision
    :param fontsize: assign the fontsize of label
    :param num: assign the number you place on the image
    :return: None
    """
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


def input_func(default):
    """
    A way to get input and set the default value
    :param default: assign the default value if input is ""(nothing)
    :return: the content you input or the default value if you do not input
    """
    inp = input(": ")
    if not inp:
        inp = default
    else:
        pass
    return inp


# Get your Twitter API credentials
def read_twit_cred(filename):
    """
    read the credential of twitter API from a text file
    (better to save in the same folder with this program if you do not want to assign the direction)
    :param filename: the name of text file(maybe need to include the direction)
    :return: the content read from text file
    """
    credential = io.open(filename, 'r')
    temp = credential.read().splitlines()
    credential.close()
    return temp


# ====================mini project 3 part==============================
def write_to_table(name, number, limit, url, label_all):
    image_number = min(number, limit)
    url_fin = url[:image_number]
    time = str(datetime.datetime.now())
    # val = None
    i = 0
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="yourpassword",
        auth_plugin='mysql_native_password',
        database="mini_project_3"
    )
    mycursor = mydb.cursor()

    # sql = "INSERT INTO customers (user, time, image_number, image_url) " \
    #       "VALUES (%s, %s, %s, %s)"
    for url_temp in url_fin:
        sql = "INSERT INTO customers (user, time, image_number, image_url, " \
              "descriptor0, descriptor1, descriptor2, descriptor3, descriptor4, " \
              "descriptor5, descriptor6, descriptor7, descriptor8, descriptor9) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, time, image_number, url_temp,
               " ", " ", " ", " ", " ", " ", " ", " ", " ", " ")
        # val = (name, str(datetime.datetime.now()), image_number, url_temp)
        mycursor.execute(sql, val)
        mydb.commit()
        j = 0
        # print(label_all)
        for label in label_all[i]:
            sql = "UPDATE customers SET descriptor"+str(j)+" = %s WHERE image_url = %s"
            val = (label, url_temp)
            mycursor.execute(sql, val)
            mydb.commit()
            j += 1
        i += 1
    pass


# this is the main part of program
# ---------------------------------------------------
# get the user name of the account
def main():
    print("please enter the use name you want(default press Enter)")
    name = input_func('@ZhongyuanCai')
    print("account is ", name)

    # get content from twitter
    twitter_content = get_all_tweets(name, 'twitter_api.txt')  # @ZhongyuanCai

    # extract url from content
    url = get_media_url(twitter_content)

    # get the number of image you want
    print("how many images do you want(default press Enter, all images)")
    number = input_func(len(url))
    print("number of images is", number)

    # add limitation to number
    print("if you want to add limitation to the number of files, please enter,(default press Enter, 100 images)")
    limit = input_func(100)
    print("the number of images limitation is ", limit)
    # download media from url
    download_media(url, int(number), int(limit))

    # get the size and reshape images
    print("please input the width of image(default press Enter)")
    width = input_func(1024)
    print("please input the hight of image(default press Enter)")
    hight = input_func(768)
    print("width is ", width, 'hight is', hight)
    resize_image("./images/", int(width), int(hight))  # 1024, 768

    # get label of images from google vision
    label = get_label("./images")
    print("please input the fontsize of label(default press Enter)")

    # assign the fontsize and number of label, then place them on images
    fontsize = input_func(50)
    print("fontsize is ", fontsize)
    print("please input the number of label you want to add on the image(default press Enter)")
    num = input_func(3)
    add_label("./images", label, int(fontsize), int(num))  # 50, 3

    # assign the parameter of video and generate video
    print("input video framerate(default press Enter)")
    framerate = input_func('1/5')
    print("input image files direction(default press Enter)")
    cd = input_func('./images/image%d.jpg')
    print("input the name and format of the video")
    out = input_func('out.mp4')
    print("the video "+out+" will convert image from "+cd+" in framerate "+framerate)
    generate_video(framerate, cd, out)

    # You are All Set if you were here
    print("All set!")

    write_to_table(name, number, limit, url, label)


if __name__ == "__main__":
    main()
