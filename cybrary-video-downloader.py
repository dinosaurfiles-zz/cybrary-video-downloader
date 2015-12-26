import re
import sys
import urllib
import urllib2
import requests
import cookielib
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

#Global Variables
courselist = {};
courseselectionlist = {};
selectedcourse = None
selectedcourselink = None
videoquality = None

def login(username, passwd):
    session = requests.session()

    values = {
        'log': username,
        'pwd': passwd,
        'testcookie': 1,
        'wp-submit': 'Log+In',
        'redirect_to': ''
    }

    r = session.post('https://www.cybrary.it/wp-login.php', data=values)
    r = session.get('https://www.cybrary.it/courses/')

    opentxt=open('course.txt','r')
    readtxt=opentxt.read()

    get_course_list(r.text)

def get_course_list(html):
    find = re.compile('<a href="https?://www.cybrary.it/course/\w+(?:-[\w]+)*/">(?:\w|\+| )+</a>')
    coursematch = list(set(find.findall(html)))
    for i in range (len(coursematch)):
        getelements = BeautifulSoup(coursematch[i], 'html.parser')
        getelements = getelements.find_all('a')
        for link in getelements:
            coursename = str(link.contents[0])
            courselink = link.get('href')
            courselist[coursename] = courselink

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

    print "\n\n Downloading Course Videos of",courseselectionlist[selectedcourse]
    selectedcourselink = courselist[courseselectionlist[selectedcourse]]
    print " Course Link:",selectedcourselink

def selectquality():
    quality = input("\n Select Video Quality: 360p/720p: ")

    while quality != 360 and quality != 720 :
        print " Error! Select an appropriate video quality"
        quality = input("\n Select Video Quality: 360p/720p: ")
    videoquality = quality

def getmodules():
    #r = session.get(selectedcourselink)
    #readtxt = r.text
    opentxt1=open('testselectedcourse.txt','r')
    readtxt1=opentxt1.read()
    #print readtxt1
    moduletable = BeautifulSoup(readtxt1, 'html.parser')
    modulediv = moduletable.find('div', class_="modulelisting")
    test0 = str(modulediv)

    find = re.compile('https?://www.cybrary.it/video/\w+(?:-[\w]+)*/')
    modulematch = list(set(find.findall(test0)))
    for i in range (len(modulematch)):
        print modulematch[i]
        #Download Video here


def main():
    #username = raw_input("Enter Username: ")
    #passwd = raw_input("Enter Your Password: ")
    #login(username,passwd)
    opentxt=open('testcourse.txt','r')
    readtxt=opentxt.read()
    #get_course_list(readtxt)
    #courseselection()
    #selectquality()
    getmodules()

    #exit = raw_input("Exit")

if __name__ == '__main__':
	main()
