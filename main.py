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
def GetLinks(soup, queue, depth):
    fin_stream = soup.find('div', {'id': 'Fin-Stream'})
    if fin_stream:
        for li in fin_stream.find_all('li'):
            a_tag = li.find('a', href=True)
            if a_tag and 'https://' in a_tag['href']:
                queue.append((a_tag['href'], depth + 1))
    return queue

# Input: Soup Object
# Output: All text from HTML
def GetContent(soup):
    content = []
    details = {
        'title': '',
        'author': '',
        'date': '',
        'content': ''
    }

    title_tag = soup.find('h1', {'id':'caas-lead-header-undefined'})  
    if title_tag:
        details['title'] = title_tag.get_text(strip=True)

    author_tag = soup.find('span', class_='caas-author-byline-collapse') 
    if author_tag:
        details['author'] = author_tag.get_text(strip=True)

    date_tag = soup.find('dic', {'id': 'caas-attr-time-style'})  
    if date_tag:
        details['date_published'] = date_tag.get_text(strip=True)

    for p in soup.find_all('p'):
        content.append(p.get_text())
    details['content'] = ' '.join(content)

    return details
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
def CreateDictionary(link, details):
    dictionary = {
        "link": link,
        "title": details['title'],
        "author": details['author'],
        "date": details['date'],
        "content": details['content']

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

    #Testing Arguments
    # print("Testing Args")
    # print(args.hops)
    # print(args.pages)
    # print(args.seed)
    # print(args.out)
    # print(args.threads)

    # Set Up Link Queue
    queue = [(args.seed, 0)]


    # Create JSON file
    CreateFile(args.out)

    # URL of the webpage you want to scrape
    url = args.seed
    # Parse the HTML content of the page
    soup = GetHTML(url)

    # Get Root Content
    content = GetContent(soup)

    # Create Root Dict
    dictionary = CreateDictionary(url, content)

    # Add Dictionary to JSON file
    AddToFile(args.out, dictionary)

    # Get all links from root
    queue = GetLinks(soup, queue, 0)
    
    #Counter initialized at 2 to account for seed page + first page in loop
    pageCounter = 2
    MAXIMUM_PAGES = int(args.pages)
    MAXIMUM_HOPS = int(args.hops)


    for link, depth in queue:

        print("Link: ", link, "Depth: ", depth)
        
        # Check for number of pages scraped, stop if limit reached
        if pageCounter > MAXIMUM_PAGES:
            print("Maximum page count exceeded!")
            break

        # Check for file size and if exceeded stop scraping
        if CheckFileSize(args.out) > 50000000:
            print("Output file size limited exceeded!")
            break

        article_soup = GetHTML(link)
        article_details = GetContent(article_soup)
        dictionary = CreateDictionary(link, article_details)
        AddToFile(args.out, dictionary)

        # Parse the HTML content of the page
        soup = GetHTML(link)

        # Get Content
        content = GetContent(soup)

        # Create Dict
        dictionary = CreateDictionary(link, content)

        #Check current depth, queue links from page if within MAXIMUM_HOPS
        if depth < MAXIMUM_HOPS:
            print("Adding links to queue")
            print("Queue size: ", len(queue))
            GetLinks(soup, queue, depth)

        # Add Dictionary to JSON file
        AddToFile(args.out, dictionary)

        pageCounter = pageCounter + 1

    # Finish Writing to file
    FinishWritingFile(args.out)
    
    # Print file size at end of script
    print("File Size is :", CheckFileSize(args.out), "bytes")

main()