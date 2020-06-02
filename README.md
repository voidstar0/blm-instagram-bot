# blm-instagram-bot
 Instagram bot that informs users using the BlackLivesMatter tag to post solid images that they may be accidentally hiding important information about the movement.
![Demonstration 1](https://i.imgur.com/cbW2vEY.png)
![Demonstration 2](https://i.imgur.com/nsYbHJl.png)

Uses a Google Cloud Function called [blm-cloud-function](https://github.com/char/blm-cloud-function) to determine if the image is a solid black image. This is to offload the image processing to the cloud and hopefully keep things running smooth.

## To-Do
1. Use multiple accounts to rotate and avoid being rate limited by Instagram.
2. Use a better way to detect solid images (Currently just checks if all RGB values are under 20)
