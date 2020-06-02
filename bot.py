from instagram_private_api import Client, ClientCompatPatch
from dotenv import load_dotenv, find_dotenv
import json
import requests
import os
import time
import ssl
import schedule
ssl._create_default_https_context = ssl._create_unverified_context


load_dotenv(find_dotenv())

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
        for post in feed["items"]:
            with open("./commentlog.txt", "r") as log:
                cached = log.read()
            print(cached)

            if str(post['code']) not in cached:
                print(f"{post['code']} not in cache")
                if 'image_versions2' in post:
                    try:
                        url = post['image_versions2']['candidates'][0]['url']
                        res = requests.post(
                            os.getenv("CLOUD_FUNCTION_URL"), data={'img_url': url})
                        json_res = res.json()
                        if json_res['solid']:
                            code = post['code']
                            print(code)
                            if 'comment_count' in post and post['comment_count'] > 0:
                                for comment in post['preview_comments']:
                                    if "please dont use the blacklivesmatter tag" in comment['text'].lower():
                                        contains_comment = True
                                        break
                                if not contains_comment:
                                    print('Solid image found. Informing user on post %s' % code)
                                    client.post_comment(post['id'], MESSAGE)
                                    # ADDED: log the url if we make a comment
                                    print("Successful Comment")
                                    with open("./commentlog.txt", "a") as log:
                                        log.write(str(str(code)+","))
                                    print("Post has been logged")
                                else:
                                    print('Bot has already commented on post: %s' % code)
                                contains_comment = False
                            else:
                                print('Solid image found. Informing user on post %s' % code)
                                client.post_comment(post['id'], MESSAGE)
                                print("Successful Comment")
                                # ADDED: log the url if we make a comment
                                with open("./commentlog.txt", "a") as log:
                                    log.write(str(str(code) + ","))
                                print("Post has been logged")
                    except Exception as e:
                        print(f'Ran into an exception (IG may be rate limiting) {e}')
                        continue
            if len(feed) == 1:
                feed = client.feed_tag('blacklivesmatter', client.generate_uuid())

