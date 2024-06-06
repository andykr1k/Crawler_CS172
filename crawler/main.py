from bs4 import BeautifulSoup
import requests
import argparse
import os
import json
from queue import Queue
from multiprocessing import Process


def get_length_utf8(s):
    """Returns the size of a string in bytes (utf-8)."""
    return len(s.encode('utf-8'))


def get_html(url):
    """Returns a BeautifulSoup object with the HTML response of the given URL."""
    print("Scraping:", url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        add_html_to_folder(soup)
        return soup
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return None


def get_links(soup, queue, depth):
    """Adds links from the given BeautifulSoup object to the queue, incrementing the depth."""
    fin_stream = soup.find('div', {'id': 'Fin-Stream'})
    if fin_stream:
        for li in fin_stream.find_all('li'):
            a_tag = li.find('a', href=True)
            if a_tag and 'https://' in a_tag['href'] and 'a.beap.gemini.' not in a_tag['href']:
                if a_tag['href'] not in list(queue.queue):
                    queue.put((a_tag['href'], depth + 1))
    return queue


def get_depth_links(soup, queue, depth, hops, base_url):
    """Adds links from the given BeautifulSoup object to the queue up to the specified hops."""
    if depth >= hops:
        return queue
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'https://' not in href:
            href = base_url + href
        if href not in list(queue.queue):
            queue.put((href, depth + 1))
    return queue


def get_content(soup):
    """Extracts and returns the content details from the given BeautifulSoup object."""
    details = {
        'title': soup.find('title').string if soup.find('title') else '',
        'author': soup.find('span', class_='caas-author-byline-collapse').get_text(strip=True) if soup.find('span', class_='caas-author-byline-collapse') else '',
        'date': soup.find('div', class_='caas-attr-time-style').find('time').get_text() if soup.find('div', class_='caas-attr-time-style') and soup.find('div', class_='caas-attr-time-style').find('time') else '',
        'content': ' '.join(p.get_text() for p in soup.find_all('p'))
    }
    return details


def create_file(file_name):
    """Creates a new JSON file and writes an opening bracket."""
    with open(file_name, "w") as f:
        f.write('[\n')


def add_html_to_folder(soup):
    """Saves the HTML content of the given BeautifulSoup object in the HTML_Pages folder."""
    html_string = soup.prettify()
    page_title = (soup.find('title').string if soup.find(
        'title') else "error").replace(" ", "_").replace("/", "_").replace("\\", "_")
    file_name = f"{page_title}.html"
    folder_name = "HTML_Pages"
    file_path = os.path.join(folder_name, file_name)
    print("HTML added to path:", file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_string)


def add_to_file(file_name, dictionary):
    """Appends a JSON dictionary to the file, followed by a comma."""
    with open(file_name, "a") as f:
        f.write(",\n")
        json.dump(dictionary, f)


def finish_writing_file(file_path):
    """Appends a closing bracket to the JSON file."""
    with open(file_path, "a") as f:
        f.write('\n]')


def create_dictionary(link, details):
    """Creates and returns a dictionary with the given link and content details."""
    return {
        "link": link,
        "title": details['title'],
        "author": details['author'],
        "date": details['date'],
        "content": details['content']
    }


def check_file_size(file_name):
    """Returns the size of the specified file in bytes."""
    return os.path.getsize(file_name)


def scrape_process(queue, output_file, maximum_bytes, maximum_hops, base_url, max_pages):
    """Main scraping process."""
    while not queue.empty() and max_pages > 0:
        link, depth = queue.get()
        print("Link:", link, "\nDepth from root:", depth)

        print("File Size:", check_file_size(output_file), "\n")
        if check_file_size(output_file) > maximum_bytes:
            print("Output file size limit exceeded!")
            break

        max_pages -= 1

        soup = get_html(link)
        if soup is None:
            continue

        content = get_content(soup)
        dictionary = create_dictionary(link, content)

        if depth < maximum_hops:
            print("Adding links to queue")
            print("Queue size:", queue.qsize())
            queue = get_depth_links(soup, queue, depth, maximum_hops, base_url)

        add_to_file(output_file, dictionary)
        queue.task_done()


def main():
    """Main function to parse arguments and initiate the scraping process."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--hops', required=True, type=int,
                        help='Number of hops from seed')
    parser.add_argument('--seed', required=True, type=str, help='Seed URL')
    parser.add_argument('--out', required=True, type=str,
                        help='Output file path')
    parser.add_argument('--threads', type=int, default=1,
                        help='Number of threads')
    parser.add_argument('--mb', type=float, default=10,
                        help='File size limit for output in MB')
    parser.add_argument('--pages', type=int, default=100,
                        help='Max number of pages to scrape')

    args = parser.parse_args()
    max_hops = args.hops
    max_bytes = args.mb * 1_000_000
    threads_count = args.threads
    output_file = args.out
    seed_url = args.seed
    max_pages = args.pages

    try:
        response = requests.head(seed_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error:", e)
        return

    queue = Queue()
    create_file(output_file)

    soup = get_html(seed_url)
    if soup is None:
        return

    content = get_content(soup)
    dictionary = create_dictionary(seed_url, content)
    add_to_file(output_file, dictionary)
    max_pages -= 1

    queue = get_links(soup, queue, 0)

    processes = []
    for _ in range(threads_count):
        p = Process(target=scrape_process, args=(
            queue, output_file, max_bytes, max_hops, seed_url, max_pages))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    finish_writing_file(output_file)
    print("File Size is:", check_file_size(output_file), "bytes")


if __name__ == "__main__":
    main()