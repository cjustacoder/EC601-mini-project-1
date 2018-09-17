#!/usr/bin/env python
# encoding: utf-8
# Author - Prateek Mehta


import tweepy  # https://github.com/tweepy/tweepy
import json
import wget
import urllib.request
import random
import string


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))


# Twitter API credentials
consumer_key = "S8LcuILJeofVWZkBilWkYrOYH"
consumer_secret = "he3oZTTPxDJG3XQdcWCRn16pSwEGfemX5grABi8NwF5LXC4Vbt"
access_key = "1039257149103394816-0nLYN7S16Ie1DflHcVgmotONLPmiBk"
access_secret = "LGikjWWaCVHQZ9SzBXRrEOlrE0lLfX2RiotNh5KDQuUIn"


def get_all_tweets(screen_name):
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
    for apple in media_files:
        json.dump(media_files, filefile)
    print("done")
    filefile.close()
    return media_files


def download_media(media_files):
    location = "./images/"
    i = 1
    leng = len(media_files)
    for res in media_files:
        name = random_string(10) + ".jpg"
        urllib.request.urlretrieve(res, location + name)
        print("downloading Numb.", i, '/', leng)
        i += 1
    print("finishing download")


twitter_content = get_all_tweets("@ZhongyuanCai")
url = get_media_url(twitter_content)
download_media(url)



