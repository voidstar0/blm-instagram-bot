# blm-instagram-bot
Instagram bot that informs users using the BlackLivesMatter tag to post solid images that they may be accidentally hiding important information about the movement.
![Demonstration 1](https://i.imgur.com/cbW2vEY.png)
![Demonstration 2](https://i.imgur.com/nsYbHJl.png)

Uses a Google Cloud Function called [blm-cloud-function](https://github.com/char/blm-cloud-function) to determine if the image is a solid black image. This is to offload the image processing to the cloud and hopefully keep things running smooth.


## Setup
You need Python 3 and `pip`. On Ubuntu: `sudo apt install python3-dev python3-pip` will get you there. You will use `python3` and `pip3` in place of `pip` and `python`, unless you override which the default is with your `$PATH` variable.

1. Create a burner account or two. Edit accounts.json to include their login information.
1. Edit the bios to include relevant information. [Example](https://www.instagram.com/blmprotectthetag/)
1. Run `pip install -r requirements.txt`. If you are not on Windows, comment out the lines with `pywin32` and `pypiwin32`.
1. Run `python3 bot.py`. If you get a missing module error, `python3 -m pip install -r requirements.txt` and try again.

## To-Do
1. Poll the tag. Right now it only goes through the current posts and stops.

Make sure you're using Python 3.5 or greater.
