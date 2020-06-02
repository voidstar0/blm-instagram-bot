from ratelimiter import RateLimiter
from instagram_private_api import Client, ClientCompatPatch
from dotenv import load_dotenv, find_dotenv
import json
import requests
import os
from time import sleep
from random import randint, choice
from color_it import *
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


rate_limiter = RateLimiter(max_calls=1, period=5.0)

clients = []
feed = []
contains_comment = False
comments = [
    'Hi, please dont use the blacklivesmatter tag as it is currently blocking important info from being shared. '
    'Please delete and repost with #BlackoutTuesday instead (Editing the caption wont work). '
    'If you want other ways to help please check out our bio. Thank you :)',

    'Please use the #blackouttuesday instead of blacklivesmatter if you' 're posting a black square. '
    'Please delete and repost with #BlackoutTuesday instead (Editing the caption wont work). '
    'If you want other ways to help please check out our bio. Thank you :)',

    'It appears you have posted a black square in the wrong hashtag blacklivesmatter is used to spread critical information. '
    'Please delete and repost with #BlackoutTuesday instead (Editing the caption wont work). '
    'If you want other ways to help please check out our bio. Thank you :)',

    'Posting black screens is hiding critical information please delete your image and repost it with the #BlackoutTuesday instead. '
    'If you want other ways to help please check out our bio. Thank you :)'
]


load_dotenv(find_dotenv())
init_color_it()


# login to instagram
with open('./accounts.json') as f:
    data = json.load(f)
    for acc in data:
        print('Logging in with username %s' % acc['username'] + '\n')
        client = Client(acc['username'], acc['password'])
        clients.append(client)
        feed = client.feed_tag('blacklivesmatter', client.generate_uuid())

# Goes over the pictures in the black lives matter hashtag
while len(feed) != 0:
    for client in clients:
        with rate_limiter:
            print('Looking for an image... \n')
            post = feed['items'].pop(0)
            print('Found ' + str(feed['num_results']) + ' images. \n')

            wait_time = randint(10, 30)
            print(color('Waiting ' + str(wait_time) + ' sec. \n', colors.YELLOW))
            sleep(wait_time)

            print('Analyzing post ' + post['code'] + ' ...\n')

            if 'image_versions2' in post:
                try:
                    url = post['image_versions2']['candidates'][0]['url']
                    res = requests.post(os.getenv("CLOUD_FUNCTION_URL"), data={'img_url': url})
                    json_res = res.json()

                    # check if the image is a black square
                    if json_res['solid']:
                        code = post['code']
                        if 'comments_disabled' in post:
                            print('Bot cannot comment on post due to disabled comments: %s' % code)
                            continue
                        if 'comment_count' in post and post['comment_count'] > 0:
                            for comment in post['preview_comments']:
                                if "If you want other ways to help please check out our bio. Thank you :)" in comment['text'].lower():
                                    contains_comment = True
                                    continue
                            if not contains_comment:
                                print(color('Solid image found. Informing user on post %s' % code + '\n', colors.ORANGE))
                                client.post_comment(post['id'], choice(comments))
                                print(color('commented successfully. \n', colors.GREEN))
                            else:
                                print('Bot has already commented on post: %s' % code)
                                contains_comment = False
                        else:
                            print(color('Solid image found. Informing user on post %s' % code + '\n', colors.ORANGE))
                            client.post_comment(post['id'], choice(comments))
                            print(color('commented successfully. \n', colors.GREEN))
                    else:
                        print('Image isn''t a black square.. moving on the next..')

                except Exception as e:
                    if hasattr(e, 'error_response') and 'spam": true,' in e.error_response:
                        print(color("Error : Commented too many times. \n", colors.RED))
                    else:
                        print(color(repr(e) + '\n', colors.RED))
                    continue

            if len(feed) == 1:
                feed = client.feed_tag('blacklivesmatter', client.generate_uuid())
