import sys
import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

print("===========================================================")
print("Twitter GuardianNET (0.10 Well Damn)")
print("Written by Deviance - Twitter: @DevianceLe")
print("============================================================")

# Set timeout value to stop scraping
timeout = 60

# Scrolling Pause Interval (2-4 is a sweet spot)
scroll_pause_time = 4

# Grabbing Screenname From Terminal
if len(sys.argv) < 2:
    print("Please provide a screen name as a command line argument.")
    sys.exit(1)

screename = sys.argv[1]
screensave = screename + '.txt'
iamlazyatm = screename + '.mp4'

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
#thisurl = 'https://twitter.com/' + screename
thisurl = 'https://twitter.com/' + screename + '/with_replies'
driver.get(thisurl)
print('Fetching', screename)
print('=======================')

# Set start time
start_time = time.time()

# Initialize an empty list to store URLs
urls = []

# Set output video file name
output_video = iamlazyatm

# Start ffmpeg to record the WebDriver
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'x11grab',            # Input format
    '-framerate', '25',         # Frame rate (adjust as needed)
    '-video_size', '1440x900',  # Video size (adjust as needed)
    '-i', ':0.0',               # Input source (screen 0, change if needed)
    '-c:v', 'libx264',          # Output video codec
    '-preset', 'ultrafast',     # Encoding preset (adjust as needed)
    '-y', #beacuseoverwrite
    output_video
]

try:
    # Start recording
    recording_process = subprocess.Popen(ffmpeg_cmd)

    # Scrolling until it stops or timeout occurs
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Grab the urls now
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for link in soup.find_all('a', href=True):
            href = link['href']
            url = 'https://twitter.com' + href.split('?')[0]
            exclude_strings = ["/analytics", "/photo", "/video", "/media", "/likes", "/following", "/header_photo", "/followers"]
            if not any(exclude_str in url for exclude_str in exclude_strings) and "/status/" in url:
                urls.append(url)

        # Check if timeout has occurred or scrolling reached the end
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout or new_height == last_height:
            break
        last_height = new_height

finally:
    # Ensure the recording process is terminated
    recording_process.terminate()

# Kill the browser
driver.quit()
os.system("killall chrome")

# Save the URLs to a file
print('=======================')
print('Scrolling finished!')
print('=======================')
with open(screensave, "w") as f2:
    for url in urls:
        f2.write(url + '\n')

print("-----------------------------")
print("Adding Urls to Archivebox")
print("-----------------------------")
os.system("archivebox add < " + screensave)

print("-----------------------------")
print("We are done here! Goodnight!")
print("-----------------------------")

