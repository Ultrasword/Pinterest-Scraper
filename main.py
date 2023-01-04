
# ----------------------------------- #
# imports

import os
import requests
from bs4 import BeautifulSoup

# ----------------------------------- #
# pre-setup

def read_file_contents(fname):
    """Read the file contents"""
    with open(fname, 'r') as f:
        data = f.read()
    return data


print("FIGURE OUT A WAY TO NOT BE A BOT!!! -- check logs / stuff sent in initial ping")
PAYLOAD = {}
HEADERS = {
    "cookie": read_file_contents("cookie"),
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "referer": "https://www.pinterest.ca/",
    "sec-ch-ua": '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }

# ----------------------------------- #
# functions

def store_soup_in_file(soup, fname):
    """Store the soup in a file"""
    # encoding issues solved: https://bobbyhadz.com/blog/python-unicodeencodeerror-charmap-codec-cant-encode-characters-in-position
    enc = 'utf-8'
    with open(fname, 'w', encoding=enc) as f:
        data = str(soup.prettify())
        ff = lambda o: str(o).encode(encoding=enc, errors="backslashreplace").decode(encoding=enc)
        print(*map(ff, data), file=f, sep="")

def load_soup_from_file(fname):
    """Load the soup from a file"""
    enc='utf-8'
    with open(fname, 'r', encoding=enc) as f:
        data = f.read()
        soup = BeautifulSoup(data, 'html.parser')
    return soup

def load_soup_from_website(link):
    """Load the soup from a website"""
    # r = requests.get(link)
    r = requests.request("GET", link, headers=HEADERS, data=PAYLOAD)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def extract_links_from_passage(passage, prefix="https://i.pinimg.com/"):
    """Extract links from a passage"""
    results = []
    index = 0
    while index < len(passage):
        index = passage.find(prefix, index)
        # while within bounds --> continuous shorten string and look through
        # 1. find end of first link
        end = passage.find('"', index+1)
        # 2. extract link
        link = passage[index:end]
        # 3. append link
        results.append(link)
        # check if more links
        cc = passage.find(prefix, end)
        # print('chekcing', index, end, '|', cc, '|', repr(passage[end:]))
        if cc < 1: break
        index = end + 1
    return list(set(results))

def download_image_from_link(link):
    """Download the image from the link"""
    fname = f"assets/{link.split('/')[-1]}"
    if os.path.exists(fname):
        return print(f"File already exists for: | {fname}")
    image_data = requests.get(links[0]).content
    save_image_bytedata(image_data, fname)

def save_image_bytedata(data, fname):
    """Save the image bytedata"""
    with open(fname, 'wb') as f:
        f.write(data)

def download_multiple_images_from_links(links):
    """Download multiple images from links"""
    input("Do not use for pinterest! All the resulting files will be the same! [also low res] [enter to continue]")
    for link in links:
        download_image_from_link(link)

# ----------------------------------- #
# tests
"""
Outline:
1. link --> get html source
2. prettify beautiful soup --> string
3. since the main image is always the first one, we can just get the first one # __ THIS IS NOT TRUE ANYMORE!!! GOTTA FIND A WAY TO PARSE
    a. index = string.find(key) : key = 'https://i.pinimg.com/'
    b. find up to 300 chars after the index, then parse for the first link
4. download the image
"""


# link = 'https://www.pinterest.ca/pin/1013591459862217259/'
link = input("Input a Pinterest link: ")
soup = load_soup_from_website(link)
# store_soup_in_file(soup, "assets/sample.html")

# loading saved html files
# soup = load_soup_from_file("assets/sample.html")
pretty = soup.prettify()
key = 'https://i.pinimg.com/'

# for single image
# index = pretty.find(key)
# section = pretty[index:index+300 if index+300 < len(pretty) else len(pretty)-1]
links = extract_links_from_passage(pretty, prefix=key)
print(links[0])
# print(links)
download_image_from_link(links[0])
# download_multiple_images_from_links(links)