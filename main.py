from bs4 import BeautifulSoup
import requests
import argparse
import threading
import os
import json

# Input: String
# Output: Size of string in bytes (utf-8)
def getLengthUTF8(s):
    return len(s.encode('utf-8'))

# Input: URL String
# Output: Beautiful soup object with HTML response
def GetHTML(URL):
    print("Scraping: ", URL)
    response = requests.get(URL)
    return BeautifulSoup(response.text, 'html.parser')

# Input: Soup Object and Link Queue
# Output: Queue filled with links from Soup Object
def GetLinks(soup, queue, depth):
    fin_stream = soup.find('div', {'id': 'Fin-Stream'})
    if fin_stream:
        for li in fin_stream.find_all('li'):
            a_tag = li.find('a', href=True)
            if a_tag and 'https://' in a_tag['href']:
                if 'a.beap.gemini.' not in a_tag['href']:
                    if a_tag['href'] not in queue:
                        queue.append((a_tag['href'], depth + 1))
    return queue

# Input: Soup Object and Link Queue
# Output: Queue filled with links from Soup Object
def GetDepthLinks(soup, queue, depth, hops, URL):
    if hops < depth:
        return queue
    links = soup.find_all('a')
    for link in links:
        if 'href' in link.attrs:
            if 'https://' not in link['href']:
                l = URL + link['href']
                print(l)
                if l not in queue:
                    queue.append((l, depth))
            else:
                if link['href'] not in queue:
                    print(link['href'])
                    queue.append((link['href'], depth))
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

    title_tag = soup.find('title')
    if title_tag:
        details['title'] = title_tag.string

    author_tag = soup.find('span', class_='caas-author-byline-collapse') 
    if author_tag:
        details['author'] = author_tag.get_text(strip=True)

    date_tag = soup.find('div', {'class': 'caas-attr-time-style'})
    if date_tag:
        date_tag = date_tag.find('time')
        details['date'] = date_tag.get_text()

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

# Main scraping function after seed has been scraped (Used for multithreading)
def ScrapeWrite(queue, OUTPUT_FILE, MAXIMUM_BYTES, MAXIMUM_HOPS, URL):
    while True:
        try:
            link, depth = queue.pop(0)
        except IndexError:
            break
        print("Link: ", link, "Depth: ", depth)
        print("File Size: ", CheckFileSize(OUTPUT_FILE))

        # Check for file size and if exceeded stop scraping
        if CheckFileSize(OUTPUT_FILE) > MAXIMUM_BYTES:
            print("Output file size limit exceeded!")
            break

        # Parse the HTML content of the page
        soup = GetHTML(link)

        # Get Content
        content = GetContent(soup)

        # Create Dict
        dictionary = CreateDictionary(link, content)

        # Check current depth, queue links from page if within MAXIMUM_HOPS
        if depth < MAXIMUM_HOPS:
            print("Adding links to queue")
            print("Queue size: ", len(queue))
            queue = GetDepthLinks(
                soup, queue, depth+1, MAXIMUM_HOPS, URL)

        # Add Dictionary to JSON file
        AddToFile(OUTPUT_FILE, dictionary)

    print("Thread finished.")

def main():
    # Instantiate Argument Parser
    parser = argparse.ArgumentParser()

    # Adding Arguments
    parser.add_argument('--hops', dest='hops',
                        type=str, help='Add number of hops from seed')
    parser.add_argument('--seed', dest='seed',
                        type=str, help='Add path to seed file')
    parser.add_argument('--out', dest='out',
                        type=str, help='Add output directory')
    parser.add_argument('--threads', dest='threads',
                        type=str, help='Add number of threads')
    parser.add_argument('--mb', dest='mb',
                        type=str, help='Add file size for output (MB)')

    # Getting Arguments
    args = parser.parse_args()

    if not (args.hops and args.seed and args.out):
        print("Insufficient arguments. Please include the hops, seed and out")
        return
    
    try:
        response = requests.head(URL)
        if response.status_code != 200:
            print("Invalid seed URL.")
            return
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return

    #Testing Arguments
    # print("Testing Args")
    # print(args.hops)
    # print(args.seed)
    # print(args.out)
    # print(args.threads)
    # print(args.mb)

    MAXIMUM_HOPS = int(args.hops)
    MAXIMUM_BYTES = float(args.mb) * 1000000
    THREADS = int(args.threads) if args.threads else 1
    OUTPUT_FILE = args.out
    URL = args.seed

    # Set Up Link Queue
    queue = []

    # Create JSON file
    CreateFile(OUTPUT_FILE)

    # Parse the HTML content of the page
    soup = GetHTML(URL)

    # Get Root Content
    content = GetContent(soup)

    # Create Root Dict
    dictionary = CreateDictionary(URL, content)

    # Add Dictionary to JSON file
    AddToFile(OUTPUT_FILE, dictionary)

    # Get all links from root
    queue = GetLinks(soup, queue, 0)

    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=ScrapeWrite, args=(
            queue, OUTPUT_FILE, MAXIMUM_BYTES, MAXIMUM_HOPS, URL))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # Finish Writing to file
    FinishWritingFile(OUTPUT_FILE)
    
    # Print file size at end of script
    print("File Size is :", CheckFileSize(OUTPUT_FILE), "bytes")

main()