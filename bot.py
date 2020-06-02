from instagram_private_api import Client, ClientCompatPatch
from dotenv import load_dotenv, find_dotenv
import json
import requests
import os
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from ratelimiter import RateLimiter

load_dotenv(find_dotenv())

test = False

rate_limiter = RateLimiter(max_calls=200, period=60.0);
clients = []
feed = []
contains_comment = False
MESSAGE = u'Hi, please don\'t use the blacklivesmatter tag as it is currently blocking important info from being shared. Please delete and repost with #BlackoutTuesday instead (Editing the caption wont work). If you want other ways to help please check out our bio. Thank you :)'

with open('./accounts.json') as f:
    data = json.load(f)
    for acc in data:
        print('Logging in with username %s' % acc['username'])
        client = Client(acc['username'], acc['password'])
        clients.append(client)
        feed = client.feed_tag('blacklivesmatter', client.generate_uuid())


while len(feed) != 0:
    for client in clients:
        with rate_limiter:
            post = feed['items'].pop(0)
            if 'image_versions2' in post:
                try:
                    url = post['image_versions2']['candidates'][0]['url']
                    res = requests.post(os.getenv("CLOUD_FUNCTION_URL"), data={'img_url': url})
                    json_res = res.json()
                    if(json_res['solid']):
                        code = post['code']
                        if 'comment_count' in post and post['comment_count'] > 0:
                            for comment in post['preview_comments']:
                                if "please dont use the blacklivesmatter tag" in comment['text'].lower():
                                    contains_comment = True
                                    break
                            if not contains_comment:
                                print('Solid image found. Informing user on post %s' % code)
                                if not test: client.post_comment(post['id'], MESSAGE)
                            else:
                                print('Bot has already commented on post: %s' % code)
                            contains_comment = False
                        else:
                            print('Solid image found. Informing user on post %s' % code)
                            if not test: client.post_comment(post['id'], MESSAGE)
                except KeyboardInterrupt:
                    print("Breaking loop")
                    break
                except:
                    print('Ran into an exception (IG may be rate limiting)')
                    continue
            if len(feed) == 1:
                feed = client.feed_tag('blacklivesmatter', client.generate_uuid())
