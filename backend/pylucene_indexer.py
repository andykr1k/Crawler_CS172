import logging, sys
logging.disable(sys.maxsize)

import lucene
import os
import argparse
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
from bs4 import BeautifulSoup


def read_html_files(dir):
    html_files = []
    for filename in os.listdir(dir):
        if filename.endswith(".html"):
            filepath = os.path.join(dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                html_files.append((filename, file.read()))
    return html_files

def create_index(dir, html_dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    
    for filename, c in read_html_files(html_dir): 
        soup = BeautifulSoup(c, 'html.parser')

        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.string

        author_tag = soup.find('span', class_='caas-author-byline-collapse') 
        if author_tag:
            author = author_tag.get_text(strip=True)

        date_tag = soup.find('div', {'class': 'caas-attr-time-style'})
        if date_tag:
            date_tag = date_tag.find('time')
            date = date_tag.get_text()

        body = soup.get_text()

        doc = Document()
        doc.add(Field('Title', str(title), metaType))
        doc.add(Field('Body', str(body), contextType))
        writer.addDocument(doc)
    writer.close()

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('Body', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 20).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        body_text = doc.get("Body").strip()[500:2000].replace('\n', '')
        body_text = " ".join(body_text.split())

        topkdocs.append({
            "score": hit.score,
            "title": doc.get("Title").replace('\n','').replace('\t',''),
            "text": body_text
        })
    
    
    for doc in topkdocs:
        print(f"Title: {doc['title']}")
        print(f"BM25 Score: {doc['score']}")
        print("Body:")
        print(doc['text'])
        print('\n')

def main():

    print("Indexing...")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('html_path', type=str, help='Path to html_pages directory')
    parser.add_argument('index_path', type=str, help='Output file for indexed pages')
    parser.add_argument('query', type=str, help='Terms to be queried')

    args = parser.parse_args()

    index_dir = args.index_path
    html_dir = args.html_path
    query = args.query


    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    create_index(index_dir, html_dir)
    retrieve(index_dir, query)

main()