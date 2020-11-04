This project aims to help you download your favorite/likes images from Twitter and Pixiv. Everytime you run it, it will only download your latest likes into corresponding date folder in assets. 

features
* easily save your likes with highest quality without repetition and review them anytime you want.
* Put all relating information, author, title, tag, links, create date into image metadata. Never Lose It.
* Automatically generate image excerpt as `digest.png`.

# How to use it
1. If you want to download likes from twitter, you need to apply twitter api keys.
2. Install requirements. `pip install -r requirements.txt`.
3. Write your information into config.json
4. Run `main.py` in command line

# Contribution
Feel free to make it possible to download likes from other websites, like dribble.

A few things to notice:
1. Put all caches into caches folder and following the name `website_yourname_likes.json`
2. Download images into correct location
```python
    # create current date folder. Correct the date for late night.
    current_date = '0'
    if datetime.datetime.now().hour < 3:
        current_date = date.today()-datetime.timedelta(days=1)
    else:
        current_date = date.today()
    if not os.path.exists(f'assets/{current_date}'):
        os.makedirs(f'assets/{current_date}')
```
3. Put information into metadata with pyexiv2.
```python
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
```
4. Get necessary information from `config.json`.

If you don't know where to start, you can follow the code pattern of existed scripts, `plugins/pixiv/pixiv.py` and  `plugins/twitter/twitter.py`.