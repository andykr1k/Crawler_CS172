from bs4 import BeautifulSoup
import requests
import argparse
import threading
import os
import json

# Input: String
# Output: Size of string in bytes (utf-8)
def utf8len(s):
    return len(s.encode('utf-8'))

# Input: URL String
# Output: Beautiful soup object with HTML response
def GetHTML(url):
    print("Scraping: ", url)
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# Input: Soup Object and Link Queue
# Output: Queue filled with links from Soup Object
def GetLinks(soup, queue):
    content_div = soup.find('div', {'id': 'mw-content-text'})
    links = content_div.find_all('a')
    for link in links:
        if '#' not in str(link.get('href')) and 'File:' not in str(link.get('href')):
            if 'https' in str(link.get('href')):
                queue.append(str(link.get('href')))
            else:
                queue.append('https://en.wikipedia.org/' + str(link.get('href')))
    return queue

# Input: Soup Object
# Output: All text from HTML
def GetContent(soup):
    content_div = soup.find('div', {'id': 'mw-content-text'})
    return content_div.get_text().replace('\n', '')

# Input: File Name String
# Output: N/A
# Description: Function to create new file, add open bracket for JSON and close file
def CreateFile(file_name):
    f = open(file_name, "w")
    f.write('[')
    f.close()
    return

# Input: File Name String and dictionary object
# Output: N/A
# Description: Function to add a JSON dictionary to JSON file also adds comma after JSON dictionary is appended
def AddToFile(file_name, dictionary):
    f = open(file_name, "a")
    json.dump(dictionary, f)
    f.write(",")
    f.close()
    return

# Input: File Name String
# Output: N/A
# Description: Function to append a close bracket to end of file
def FinishWritingFile(file_path):
    f = open(file_path, "a")
    f.write(']')
    f.close()
    return

# Input: Link String and Content String
# Output: Dictionary
def CreateDictionary(link, content):
    dictionary = {
        "link": link,
        "content": content
    }
    return dictionary

# Input: File Name String
# Output: Size of file in bytes
def CheckFileSize(file_name):
    file_size = os.path.getsize(file_name)
    return file_size

def main():
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

    # Set Up Link Queue
    queue = []

    # Create JSON file
    CreateFile(args.out)

    # URL of the webpage you want to scrape
    url = 'https://en.wikipedia.org/wiki/Basketball'

    # Parse the HTML content of the page
    soup = GetHTML(url)

    # Get Root Content
    content = GetContent(soup)

    # Create Root Dict
    dictionary = CreateDictionary(url, content)

    # Add Dictionary to JSON file
    AddToFile(args.out, dictionary)

    # Get all links from root
    queue = GetLinks(soup, queue)

    for link in queue:

        # Check for file size and if exceeded stop scraping
        if CheckFileSize(args.out) > 50000000:
            print("Output file size limited exceeded!")
            break

        # Parse the HTML content of the page
        soup = GetHTML(link)

        # Get Content
        content = GetContent(soup)

        # Create Dict
        dictionary = CreateDictionary(link, content)

        # Add Dictionary to JSON file
        AddToFile(args.out, dictionary)

    # Finish Writing to file
    FinishWritingFile(args.out)
    
    # Print file size at end of script
    print("File Size is :", CheckFileSize(args.out), "bytes")

main()