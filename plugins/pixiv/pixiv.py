import datetime
import json
import os
from datetime import date
from pathlib import Path

from pixivapi import Client, Size
from pyexiv2 import Image

# user bookmark is sort by date, newsest on the top
# download all newsest like to assets/date folder

# edit xmp data


def xmp_edit(illust, img_path):
    img = Image(
        img_path, encoding='utf-8')
    tags = []
    for i in illust.tags:
        if i['translated_name'] == None:
            tags.append(i['name'])
        else:
            tags.append(i['translated_name'])
    print(tags)
    xmp_data = {
        'Xmp.dc.creator': [illust.user.name],
        'Xmp.dc.description': illust.caption,
        'Xmp.dc.title': illust.title,
        # 'Xmp.photoshop.Category': illust.type,
        'Xmp.photoshop.DateCreated': str(illust.create_date),
        'Xmp.photoshop.Source': f'https://www.pixiv.net/artworks/{illust.id}',
        'Xmp.xmp.Label': ','.join(tags),

    }
    img.modify_xmp(xmp_data)
    img.close()


def pixiv():
    # read config
    account = {}
    with open('config.json') as f:
        account = json.load(f)
        f.close()

    # get the last image id to continue
    old_id = ''
    if not os.path.exists('caches/pixiv_glazec_likes.json'):
        with open('caches/pixiv_glazec_likes.json', 'w') as f:
            f.close()
    else:
        with open('caches/pixiv_glazec_likes.json', 'r') as f:
            old_like = json.load(f)
            old_id = old_like['illustrations'][0]['id']
            f.close()

    # login
    client = Client(language='zh-CN')
    client.login(account['pixiv']['username'], account['pixiv']['password'])

    print('Checking Pixiv new likes....')
    # get all new bookmark image info
    current_page = client.fetch_user_bookmarks(
        account['pixiv']['id'], max_bookmark_id=None)
    likes = current_page['illustrations']
    # maximum number of image info to get
    n = 20
    k = 1
    while old_id not in [x.id for x in current_page['illustrations']] and k <= n//30:
        next_page = client.fetch_user_bookmarks(
            16139335, max_bookmark_id=current_page['next'])
        likes = likes+next_page['illustrations']
        current_page = next_page
        k = k+1
    try:
        likes = likes[:[
            x.id for x in current_page['illustrations']].index(old_id)]
    except ValueError:
        pass

    # Write new image info to like.json
    if len(likes) > 0:
        print(f'Found {len(likes)} new images')
        with open('caches/pixiv_glazec_likes.json', 'w') as f:
            json.dump({'illustrations': [{'id': x.id} for x in likes]}, f)
    else:
        print('Up to Date')

    # create current date folder. Correct the date for late night.
    current_date = '0'
    if datetime.datetime.now().hour < 3:
        current_date = date.today()-datetime.timedelta(days=1)
    else:
        current_date = date.today()
    if not os.path.exists(f'assets/{current_date}'):
        os.makedirs(f'assets/{current_date}')

    # download image by id
    for illust in likes:
        illust.download(
            directory=Path(f'assets/{current_date}'),
            size=Size.ORIGINAL,
        )
        if(illust.page_count == 1):
            try:
                xmp_edit(illust, f'assets/{current_date}/{str(illust.id)}.jpg')
            except RuntimeError:
                xmp_edit(illust, f'assets/{current_date}/{str(illust.id)}.png')
        else:
            for p in range(illust.page_count):
                try:
                    xmp_edit(
                        illust, f'assets/{current_date}/{str(illust.id)}/{str(illust.id)}_p{p}.jpg')
                except RuntimeError:
                    xmp_edit(
                        illust, f'assets/{current_date}/{str(illust.id)}/{str(illust.id)}_p{p}.png')
        print(f'Download {illust.id}')


if __name__ == "__main__":
    pixiv()
