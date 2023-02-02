import time
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests


options = webdriver.ChromeOptions()
# options.add_argument(argument='--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ----------------------------------- #
# pinterest functions

TARGETS = ['', 'hCL','kVc','L4E','MIw']
BOARD_TARGET = ['', 'Wk9', 'xQ4', 'CCY', 'S9z', 'DUt', 'kVc', 'agv', 'LIa']
BOARD_A_PARENT = ['', 'zI7', 'iyn', 'Hsu']

def download_image(link, website_link):
    """Save a link to an image file"""
    path = os.path.join('assets', website_link.strip('/').split('/')[-1] + '.' + link.split('/')[-1].split('.')[-1])
    if os.path.exists(path):  return print("Already downloaded:", link)
    print("Downloading:", link)
    response = requests.get(link)
    with open(path, 'wb') as f:
        f.write(response.content)

def image_from_pinterest(link):
    """Download an image given a pinterest link"""
    driver.get(link)
    time.sleep(0.5)
    element = driver.find_element(By.CSS_SELECTOR, '.'.join(TARGETS))
    url = element.get_attribute('src')
    download_image(url, link)

def get_board_images(board, num):
    """Download images from a pinterest board"""
    driver.get(board)
    # get the images
    objs = set()

    prevheight = 0
    height = driver.execute_script("return document.body.scrollHeight")
    
    while len(objs) < num and height - prevheight > 100:
        # data = list(driver.find_elements(By.CSS_SELECTOR, '.'.join(BOARD_A_PARENT)))
        data = list(driver.find_elements(By.TAG_NAME, 'img'))
        # print("Checking:", len(data))
        for a in data:
            if len(objs) >= num: break
            # we have image -- we want to go backwards!
            if a.get_attribute('class') == ' '.join(TARGETS[1:]):
                # recursively find the <a> tag parent
                parent = a
                try:
                    while parent.tag_name != 'a':#' '.join(BOARD_TARGET[1:]):
                        parent = parent.find_element(By.XPATH, '..')
                except: continue

                # print(parent.tag_name, parent.get_attribute('class'))
                # get the href
                url = parent.get_attribute('href')
                # print(url)
                if not url: continue
                objs.add(url)
        print("Found:", len(objs), "images so far...")

        # update height
        print("Scrolling:", height - prevheight)
        # scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Waiting 1.5 seconds for page to load -- since it is a board")
        time.sleep(2)
        
        prevheight = height
        height = driver.execute_script("return document.body.scrollHeight")
        print("New height:", height, "Prev Height:", prevheight)


    # bc selenium weird -- we must buffer everything before proceed to download all
    print("Downloading:", len(objs))
    for url in objs:
        image_from_pinterest(url)

# ----------------------------------- #
# scraping!

running = True
while running:
    data = input("Enter a pinterest link: [or 'N'/'n' to exit]\n>")
    if data.lower() == 'n':
        running = False
        break
    # split to check if pin or board
    parts = data.split('/')
    # if 'pin' == pin, else == board
    if parts[3] == 'pin':
        image_from_pinterest(data)
    else:
        # ask for how many images to download
        num = input("How many images to download? ['A'/'a' for all]\n>")
        num = (10000 if num.lower() == 'a' else int(num))
        # get the board -- all images
        get_board_images(data, num)


# ----------------------------------- #
# end
driver.close()
