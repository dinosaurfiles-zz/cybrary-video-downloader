import os
import getpass
import requests

from bs4 import BeautifulSoup

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--quality', choices=[360, 720], default=360,type=int, help="Select video quality")
parser.add_argument('--course', default="https://www.cybrary.it/course/ethical-hacking/", help="Course link")
args = parser.parse_args()

# Global Session Variables
session = requests.session()

# Initialize Login
def login(username, password):
	headers = {
		'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
	}

	values = {
		'log': username,
		'pwd': password,
		'testcookie': 1,
		'wp-submit': 'Log+In',
		'redirect_to': ''
	}

	# Submit username and password for login
	global session
	session.post('https://www.cybrary.it/wp-login.php', data=values, headers=headers)

# Parse course links and download videos
def downloadCourseVideos(quality, course):
	global session

	courseHTML = (session.get(course)).text
	parsedCourseHTML = BeautifulSoup(courseHTML, 'html.parser')

	for lessonLink in parsedCourseHTML.find_all('a', attrs={'class':'title'}):
		lessonHTML = (session.get(lessonLink.get('href'))).text
		parsedLessonHTML = BeautifulSoup(lessonHTML, 'html.parser')
		videoLink = parsedLessonHTML.find('iframe', attrs={'class':'sv_lessonvideo'})
		try:
             		downloadVideo(videoLink.get('src'), quality)
         	except Exception as e:
             		print e

# Download video using youtube-dl
def downloadVideo(videoLink, quality):
	# Apparently, cybrary.it uses vimeo to host their videos and this might change at anytime.
	# Feel free to submit an issue if errors exist

	# If windows
	if os.name == 'nt':
		command = "youtube-dl.exe -cif http-%sp %s" % (quality, videoLink)

	# *nix
	else:
		command = "youtube-dl -cif http-%sp %s --referer https://www.cybrary.it/" % (quality, videoLink)
	os.system(command)

# Main function
def main():
	username = raw_input("Username: ")
	password = getpass.getpass()
	login(username, password)
	downloadCourseVideos(args.quality, args.course)

if __name__ == '__main__':
	main()
