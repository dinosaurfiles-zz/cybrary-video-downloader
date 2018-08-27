import os
import sys
import getpass
import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()

parser.add_argument('--quality',
                    choices=[360, 720],
                    default=360,
                    type=int,
                    help="Select video quality"
                    )

parser.add_argument('--course',
                    default="https://www.cybrary.it/course/ethical-hacking/",
                    help="Course link"
                    )

args = parser.parse_args()
session = requests.session()


# Initialize Login
def login(username, password):

    params = {
        'log': username,
        'pwd': password,
        'r3f5x9JS': 'https%3A//www.cybrary.it/',
        'redirect_to': 'https://www.cybrary.it',
        'testcookie': 1,
        'wp-submit': 'Log In'
    }

    # Submit username and password for login

    global session
    connect = session.post('https://www.cybrary.it/wp-login.php', data=params)
    cookies = connect.cookies.get_dict()

    if len(cookies.keys()) != 6:
        sys.exit('invalid parameters')


def download_course_videos(quality, course):
    global session

    course_html = (session.get(course)).text
    parsed_course_html = BeautifulSoup(course_html, 'html.parser')

    for lesson_tag in parsed_course_html.find_all(
            'a', attrs={'class': 'modulehover'}
    ):
        lesson_html = session.get(lesson_tag.get('href'))
        parsed_lesson_html = BeautifulSoup(lesson_html.text, 'html.parser')
        for video_tag in parsed_lesson_html.findAll(
                'iframe', attrs={'id': 'lessonPlayer'}
        ):
            download_video(video_tag.get('src'), quality)


def download_video(video_link, quality):
    if os.name == 'nt':
        command = ("youtube-dl.exe -cif http-%sp %s --referer "
                   "https://www.cybrary.it/" % (quality, video_link))
    else:
        command = ("youtube-dl -cif http-%sp %s --referer "
                   "https://www.cybrary.it/" % (quality, video_link))

    os.system(command)


# Main function
def main():
    username = input("Username: ")
    password = getpass.getpass()
    login(username, password)
    download_course_videos(args.quality, args.course)


if __name__ == '__main__':
    main()
