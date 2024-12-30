from git import Repo
import cv2
from datetime import date
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

REPO_PATH = os.path.dirname(os.path.abspath(__file__))  # Current script directory

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--force-dark-mode")  # Forces dark mode
chrome_options.add_argument("--enable-features=WebContentsForceDark")  # Forces web content to dark mode


def MakeCommit():
    # GitHub Configuration
    REPO_URL = 'https://github.com/git-hub-paint/GitPaint.git'


    # Step 1: Initialize and Commit Changes Locally
    repo = Repo.init(REPO_PATH)
    origin = None

    # Check if 'origin' remote exists
    if 'origin' not in [remote.name for remote in repo.remotes]:
        origin = repo.create_remote('origin', REPO_URL)
    else:
        origin = repo.remote(name='origin')

    # Stage and commit changes
    repo.git.add('--all')
    repo.index.commit('Automated commit via GitPython')

    # Step 2: Push to GitHub
    try:
        origin.push(refspec='HEAD:refs/heads/main')
        print(f'Changes pushed to {REPO_URL}.')
    except Exception as e:
        print(f'Error during push: {e}')

def SetPixel(strength):
    if strength < 1:
        return
    for i in range(0, strength):
        MakeCommit()



def days_since_january_first():
    today = date.today()
    jan_first = date(today.year, 1, 1)
    return (today - jan_first).days

def is_2025(): 
    current_year = date.today().year
    return current_year == 2025

def GetTodayPixel():
    days=days_since_january_first()

    x=days//7
    y=days%7

    if x>52:
        return -1
    
    if not is_2025():
        return -1

    image = cv2.imread(REPO_PATH+'/image_to_draw.png')
    height, width = image.shape[:2]

    print(x,y)

    green_value = image[y, x][1]  # [1] is the green channel in BGR format
    return round(green_value/255*4.5)


#-----------------Main-----------------
#This part runs once per day on the rasberry pi
#--------------------------------------

#Set the pixel
SetPixel(GetTodayPixel())

#Wait for the commit to be pushed
time.sleep(2)

#Open Browser, take a screenshot
driver = webdriver.Chrome(options=chrome_options)  # Or webdriver.Firefox()
driver.get('https://github.com/git-hub-paint')
driver.maximize_window()
time.sleep(10)
driver.save_screenshot(REPO_PATH+'/proof/'+str(days_since_january_first())+'.png')
driver.quit()

