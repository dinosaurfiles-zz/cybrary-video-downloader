import os
import re
import getpass
import requests
from bs4 import BeautifulSoup

### Global Variables
courselist = {};
courseselectionlist = {};
selectedcourse = None
selectedcourselink = None
videoquality = 360
session = requests.session()

### Session Login, Get Courses
def login(username, passwd):
    values = {
        'log': username,
        'pwd': passwd,
        'testcookie': 1,
        'wp-submit': 'Log+In',
        'redirect_to': ''
    }

    sessionlink = session.post('https://www.cybrary.it/wp-login.php', data=values)
    sessionlink = session.get('https://www.cybrary.it/courses/')

    get_course_list(sessionlink.text)

### Get Courses List
def get_course_list(html):
    coursesregex = re.compile('<a href="https?://www.cybrary.it/course/\w+(?:-[\w]+)*/">(?:\w|\+| )+</a>')
    coursematch = list(set(coursesregex.findall(html)))
    for i in range (len(coursematch)):
        getelements = BeautifulSoup(coursematch[i], 'html.parser')
        getelements = getelements.find_all('a')
        for link in getelements:
            coursename = str(link.contents[0])
            courselink = link.get('href')
            courselist[coursename] = courselink

### Select A Course
def courseselection():
    print " Courses Available:"
    a = 0
    for key in sorted(courselist):
        print "\t[%d]:\t%s" % (a, key)
        courseselectionlist[a] = key
        a+=1
    selectedcourse = input(" Select a Course to Download: ")

    while selectedcourse < 0 or selectedcourse > a-1:
        print "\n No Course selected!"
        selectedcourse = input(" Select a Course to Download: ")

    print "\n Downloading Course Videos of",courseselectionlist[selectedcourse]
    global selectedcourselink
    selectedcourselink = courselist[courseselectionlist[selectedcourse]]
    print " Course Link:",selectedcourselink

### Select Video Quality
def selectquality():
    quality = input("\n Select Video Quality: 360/720: ")

    while quality != 360 and quality != 720 :
        print " Error! Select an appropriate video quality"
        quality = input("\n Select Video Quality: 360p/720p: ")
    global videoquality
    videoquality = quality

### Get Links of Each Module
def getmodules():
    modulehtml = session.get(selectedcourselink)
    moduletable = BeautifulSoup(modulehtml.text, 'html.parser')
    modulediv = moduletable.find('div', class_="modulelisting")
    divhtml = str(modulediv)

    moduletitleregex = re.compile('<a href="#">(?:\w|\+| |-|&|,)+</a>')
    moduletitle = moduletitleregex.findall(divhtml)

    modulevidregex = re.compile('https?://www.cybrary.it/video/\w+(?:-[\w]+)*/')
    moduletable = BeautifulSoup(divhtml, 'html.parser')
    modulediv = moduletable.find_all('div', class_="slide_toggle_content")

    for i in range (len(moduletitle)):
        linktag = BeautifulSoup(moduletitle[i], 'html.parser')
        contenttag = linktag.find('a')
        contenttag = contenttag.contents
        outputdirectory = os.getcwd()+"/"+contenttag[0]+"/"
        if(not os.path.isdir(outputdirectory)):
            os.mkdir(outputdirectory)
        modulevid = list(set(modulevidregex.findall(str(modulediv[i]))))
        for videourl in modulevid:
            videodownload(videourl, outputdirectory)

### Download Videos using youtube-dl
def videodownload(url, outputdirectory):
    video = session.get(url)
    videohtml = video.text

    #https://player.vimeo.com/video/999999999
    videoregex = re.search( r'https://player.vimeo.com/video/\w+', videohtml)
    if videoregex:
        outputformat = outputdirectory+"%(title)s-%(id)s.%(ext)s"
        command = "youtube-dl -cif http-%sp -o '%s' %s" % (videoquality, outputformat, videoregex.group())
        os.system(command)
    else:
        print "Something is wrong. Please contact dinosaurfiles on Github"

def main():
    username = raw_input("Enter Username: ")
    passwd = getpass.getpass()
    login(username,passwd)
    courseselection()
    selectquality()
    getmodules()

    exit = raw_input("Download Finished")

if __name__ == '__main__':
	main()
