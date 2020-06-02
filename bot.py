from instagram_private_api import Client, ClientCompatPatch

import json
import requests
import os
from time import sleep
from random import randint
from ColorIt import *



clients = []
feed = []
CLOUD_FUNCTION_URL= 'https://us-central1-protect-blm.cloudfunctions.net/isSolidColor'
comments = [
    'Hi, please dont use the blacklivesmatter tag as it is currently blocking important info from being shared. Please delete and repost with #BlackoutTuesday instead (Editing the caption wont work). If you want other ways to help please check out our bio. Thank you :)',
    'Please use the #blackouttuesday instead of blacklivesmatter if you''re posting a black square.  Please delete and repost with #BlackoutTuesday instead (Editing the caption wont work). If you want other ways to help please check out our bio. Thank you :)',
    'It appears you have posted a black square in the wrong hashtag blacklivesmatter is used to spread critical information. Please delete and repost with #BlackoutTuesday instead (Editing the caption wont work). If you want other ways to help please check out our bio. Thank you :)',
    'Posting black screens is hiding critical information please delete your image and repost it with the #BlackoutTuesday instead. If you want other ways to help please check out our bio. Thank you :)'
]

initColorIt()

#login to instagram
with open('./accounts.json') as f:
    data = json.load(f)
    for acc in data:
        print('Logging in with username %s' % acc['username'] + '\n')
        client = Client(acc['username'], acc['password'])
        clients.append(client)
        feed = client.feed_tag('blacklivesmatter', client.generate_uuid())

#Goes over the pictures in the black lives matter hashtag
while len(feed) != 0:
    for client in clients:

        print ('Looking for an image... \n')
        post = feed['items'].pop(0)        
        print ('Found ' + str(feed['num_results']) + ' images. \n')

        waitTime = randint(10,30)
        print(color('Waiting ' + str(waitTime) + ' sec. \n',colors.YELLOW))
        sleep(waitTime)

        print ('Analyzing post '+ post['code'] +' ...\n')

        if 'image_versions2' in post:
            try:
                url = post['image_versions2']['candidates'][0]['url']
                res = requests.post(CLOUD_FUNCTION_URL, data = { 'img_url': url })
                json_res = res.json()

                # check if the image is a black square
                if(json_res['solid']):
                    code = post['code']
                    print(color('Solid image found. Informing user on post %s' % code + '\n',colors.ORANGE))

                    randomlySelectedComment = randint(0,3)

                    print('Commenting comment #' + str(randomlySelectedComment) +'\n')

                    client.post_comment(post['id'], str(comments[randomlySelectedComment]))

                    print(color('commented successfully. \n',colors.GREEN))
                else: 
                    print('Image isn''t a black square.. moving on the next..')

            except Exception as e:
                if 'spam": true,' in e.error_response:
                    print(color("Error : Commented too many times. \n", colors.RED))
                else:
                    print(e)
                continue

        if len(feed) == 1:
            feed = client.feed_tag('blacklivesmatter', client.generate_uuid())
                    
