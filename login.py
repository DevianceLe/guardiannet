#This is used to create a profile and login via twitter so you can scrape 
#This was used after Elon lock down.

import sys
import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setting Browser Options
options = Options()
prefs = {
    'crashpad.enabled': False,
}
options.add_argument("--disable-infobars");
options.add_argument("--kiosk")
options.add_argument("--user-data-dir=/home/sjohns/.config/google-chrome") #Path to your chrome profile
options.add_argument("--profile-directory=Profile 1")
driver = webdriver.Chrome(options=options)
thisurl = 'https://twitter.com/'
driver.get(thisurl)
time.sleep(30)
