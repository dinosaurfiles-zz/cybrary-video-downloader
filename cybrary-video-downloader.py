#!/usr/bin/python

import os
import re
import sys
import getpass
import requests
from more_itertools import unique_everseen

# Set sys encoding to UTF-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Global Variables
session = requests.session()
lessonVideoLink = {}


# Initialize Login
def login(username, password):
    values = {
        'log': username,
        'pwd': password,
        'testcookie': 1,
        'wp-submit': 'Log+In',
        'redirect_to': ''
    }
    global session
    session.post('https://www.cybrary.it/wp-login.php', data=values)


# Get Lessons
def getLessonList(courselink):
    global session
    coursehtml = (session.get(courselink)).text

    lessonLinkRegex = re.compile(
        'https?://www.cybrary.it/video/\w+(?:-[\w]+)*/')
    matchme = list(unique_everseen(lessonLinkRegex.findall(coursehtml)))

    global lessonVideoLink
    for link in matchme:
        lessonVideoLink[link] = getVideoLink(link)


# Get Video URL
def getVideoLink(lessonlink):
    global session
    lessonhtml = (session.get(lessonlink)).text

    videoLinkRegex = re.compile('https?://player.vimeo.com/video/[\d]+')
    return (list(unique_everseen(videoLinkRegex.findall(lessonhtml))))[0]


# Download Videos using youtube-dl
def downloadVideos(quality):
    global lessonVideoLink

    for key in lessonVideoLink:
        print "Downloading %s" % (key)
        command = "youtube-dl -cif http-%sp %s" % (
            quality, lessonVideoLink[key])
        os.system(command)


def main():
    if len(sys.argv) < 3:
        print "Usage: ./cybrary-video-downloader.py <270/360/720> \"<course link>\""
        print "Example: ./cybrary-video-downloader.py 360 \"https://www.cybrary.it/course/ethical-hacking/\""
    else:
        username = raw_input("Username: ")
        passwd = getpass.getpass()
        login(username, passwd)
        getLessonList(sys.argv[2])
        downloadVideos(sys.argv[1])

if __name__ == '__main__':
    main()
