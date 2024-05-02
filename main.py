from bs4 import BeautifulSoup
import requests
import argparse

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

# URL of the webpage you want to scrape
url = 'https://example.com'

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find specific elements on the page
links = soup.find_all('a')

# Print out the links
for link in links:
    print(link.get('href'))
