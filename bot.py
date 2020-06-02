from instagram_private_api import Client, ClientCompatPatch
from dotenv import load_dotenv, find_dotenv
import json
import requests
import os
import time

from ratelimiter import RateLimiter

load_dotenv(find_dotenv())

clients = [];
feed = [];
num_accounts = 0;
ops_per_minute = 0;

with open('./accounts.json') as f:
    data = json.load(f)
    num_accounts = len(data)
    # https://developers.facebook.com/docs/graph-api/overview/rate-limiting#instagram
    ops_per_minute = 200 * num_accounts
    for acc in data:
        print('Logging in with username %s' % acc['username'])
        client = Client(acc['username'], acc['password'])
        clients.append(client)
        feed = client.feed_tag('blacklivesmatter', client.generate_uuid())

rate_limiter = RateLimiter(max_calls=ops_per_minute, period=60.0)

while len(feed) != 0:
    for client in clients:
        with rate_limiter:
            post = feed['items'].pop(0);
            if 'image_versions2' in post:
                try:
                    url = post['image_versions2']['candidates'][0]['url']
                    res = requests.post(os.getenv("CLOUD_FUNCTION_URL"), data = { 'img_url': url })
                    json_res = res.json()
                    if(json_res['solid']):
                        code = post['code']
                        print('Solid image found. Informing user on post %s' % code)
                        client.post_comment(post['id'], 'Hi, please dont use the blacklivesmatter tag as it is currently blocking important info from being shared. Please delete and repost with #BlackoutTuesday instead (Editing the caption wont work). If you want other ways to help please check out our bio. Thank you :)')
                except:
                    print('Ran into an exception (IG may be rate limiting)');
                    continue
            if len(feed) == 1:
                feed = client.feed_tag('blacklivesmatter', client.generate_uuid())
                        
