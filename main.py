from bs4 import BeautifulSoup
import requests
import argparse
import threading
import os

def utf8len(s):
    return len(s.encode('utf-8'))

# Instantiate Argument Parser
parser = argparse.ArgumentParser()

# Adding Arguments
parser.add_argument('--hops', dest='hops',
                    type=str, help='Add number of hops from seed')
parser.add_argument('--pages', dest='pages',
                    type=str, help='Add total number of pages')
parser.add_argument('--seed', dest='seed',
                    type=str, help='Add path to seed file')
parser.add_argument('--out', dest='out',
                    type=str, help='Add output directory')
parser.add_argument('--threads', dest='threads',
                    type=str, help='Add number of threads')

# Getting Arguments
args = parser.parse_args()

# Testing Arguments
# print(args.hops)
# print(args.pages)
# print(args.seed)
# print(args.out)
# print(args.threads)

# Open Output
f = open(args.out, "w")
f.close()

# URL of the webpage you want to scrape
url = 'https://en.wikipedia.org/wiki/Basketball'

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find specific elements on the page
content_div = soup.find('div', {'id': 'mw-content-text'})
links = content_div.find_all('a')

file_size = os.path.getsize(args.out)

while (file_size < 100):
    f = open(args.out, "a")
    # Appends links to file
    for link in links:
        f.write('https://en.wikipedia.org/' + str(link.get('href')) + '\n')
    f.close()
    file_size = os.path.getsize(args.out)

print("File Size is :", file_size, "bytes")
