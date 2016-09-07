# ATTENTION! (September 7, 2016)
# Sorry to be the bringer of the bad news. Unfortunately, this project might be dead. Due to
## [1] [Google's aggressive CAPTCHA](https://www.google.com/recaptcha) system which cybrary.it also uses to protect its users which they should really do. (Also I don't want to work on breaking CAPTCHAs :p )

## [2] Moving to Python 3.x might take considerable time plus [1]

# But don't fret! Cause we might...
## [3] Make a browser extension(firefox first) wich pulls all the links of the course videos. (No more CAPTCHAs but you need to be logged in into the cybrary.it website)
## [4] Ask cybrary.it to make all course videos available for download. (Currently, cybrary.it's videos are hosted on vimeo)


### Also, don't forget to follow me on github for more updates!

---
# cybrary-video-downloader (v0.3)
Downloads Course Videos From [Cybrary.it](https://www.cybrary.it/)

## Why u do diz?
This program is made for the love and passion for cybersecurity. Also for a friend who has a slow internet connection and the needs for offline learning
## For the folks at Cybrary.it
I made this program for the sole purpose that I mentioned above and kudos for all the **free and awesome** courses you offered! I know this program bypasses ads but don't worry, we will donate from time-to-time.
:hand::smile:
## Requirements:
- `Python` 2.7.x
- `more_itertools` - Install using `pip install more_itertools`
- `youtube-dl` - Install using pip `pip install --upgrade youtube_dl` or follow this [guide](https://rg3.github.io/youtube-dl/download.html).

## Usage Example:
`./cybrary-video-downloader.py 360/720 "course link"`

Ex: Download videos with 360p quality:

`./cybrary-video-downloader.py 360 "https://www.cybrary.it/course/ethical-hacking/"`
