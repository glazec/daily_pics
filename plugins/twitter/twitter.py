import tweepy
import json
import time
import ndjson
import requests
import os
import pysnooper
from datetime import date
import datetime
from pyexiv2 import Image


def xmp_edit(img_path, creator, description, title, dateCreated, source, label):
    img = Image(
        img_path, encoding='utf-8')
    tags = []
    for i in label:
        tags.append(i['text'])
    # print(tags)
    xmp_data = {
        'Xmp.dc.creator': [creator],
        'Xmp.dc.description': description,
        'Xmp.dc.title': title,
        # 'Xmp.photoshop.Category': illust.type,
        'Xmp.photoshop.DateCreated': dateCreated,
        'Xmp.photoshop.Source': source,
        'Xmp.xmp.Label': ','.join(tags),

    }
    img.modify_xmp(xmp_data)
    img.close()


def twitter():
    # read config and get creds
    with open('config.json') as f:
        data = json.load(f)
        creds = data['twitter']
        f.close()

    # get the last post id to continue
    old_ids = []
    if not os.path.exists('caches/twitter_glazec_likes.ndjson'):
        with open('caches/twitter_glazec_likes.ndjson', 'w') as f:
            f.close()
    else:
        with open('caches/twitter_glazec_likes.ndjson', 'r', encoding="utf_8") as f:
            old_likes = ndjson.load(f)
            old_ids = [i['id_str'] for i in old_likes]
            f.close()

    # get likes info
    auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])
    auth.set_access_token(creds["access_token"], creds["access_token_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    count = 0
    print('Checking twitter new likes....')

    likes = []
    for status in tweepy.Cursor(api.favorites,include_entities=True, tweet_mode='extended').items(200):
        count = count + 1
        status_id = str(status.id)
        if status_id in old_ids:
            print('Up to Date')
            break
        else:
            likes.append(status._json)
            print(f'Found {count} new likes', end='\r')
            time.sleep(60 * 15 / (15 * 200))

    # Write new likes post into likes.ndjson
    if len(likes) > 0:
        with open('caches/twitter_glazec_likes.ndjson', 'w') as f:
            ndjson.dump(likes, f)
            f.close()

    # create current date folder. Correct the date for late night.
    current_date = '0'
    if datetime.datetime.now().hour < 3:
        current_date = date.today()-datetime.timedelta(days=1)
    else:
        current_date = date.today()
    if not os.path.exists(f'assets/{current_date}'):
        os.makedirs(f'assets/{current_date}')

    # download images
    image_base_path = 'img/'
    pics = [fav for fav in likes if 'media' in fav['entities']]
    if len(pics) > 0:
        print(f'Found Total {len(pics)} likes containing medias')

    # notice gif file
    for fav in pics:
        print(fav['full_text'])
        for image in fav['extended_entities']['media']:
            img_data = requests.get(
                image['media_url']+'?format=jpg&name=4096x4096').content
            with open(os.path.join(f'assets/{current_date}', f"{image['id_str']}.jpg"), 'wb') as handler:
                handler.write(img_data)
            xmp_edit(os.path.join(f'assets/{current_date}', f"{image['id_str']}.jpg"), fav['user']['name'],
                     fav['full_text'].split('https://t.co/')[0], '', fav['created_at'], "https: // t.co/"+fav['full_text'].split('https://t.co/')[1], fav['entities']['hashtags'])
            time.sleep(60 * 15 / (15 * 200))


if __name__ == "__main__":
    twitter()
