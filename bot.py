from instagram_private_api import Client, ClientCompatPatch
from dotenv import load_dotenv, find_dotenv
import json
import requests
import os

load_dotenv(find_dotenv())

user_name = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

api = Client(user_name, password)
results = api.feed_tag('blacklivesmatter', api.generate_uuid())

for post in results['items']:
    if 'image_versions2' in post:
        url = post['image_versions2']['candidates'][0]['url']
        res = requests.post(os.getenv("CLOUD_FUNCTION_URL"), data = { 'img_url': url })
        json_res = res.json()
        if(json_res['solid']):
            code = post['code']
            print('Solid image found. Informing user on post %s' % code)
            api.post_comment(post['id'], 'Hi, please dont use the blacklivesmatter tag as its currently blocking important info from being shared. You should instead use #BlackoutTuesday. Thank you :)')
            
