import os
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import sys
import lucene
from org.apache.lucene.store import SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader, IndexHandler
from org.apache.lucene.search import IndexSearcher

app = Flask(__name__)

index_dir = os.path.join(os.getcwd(), 'index')

os.chdir("../")

html_dir = os.path.join(os.getcwd(), 'crawler', 'HTML_Pages')

os.chdir(os.path.join(os.getcwd(), 'backend'))

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
        title = title_tag.string if title_tag else 'No Title'

        author_tag = soup.find('span', class_='caas-author-byline-collapse')
        author = author_tag.get_text(strip=True) if author_tag else 'No Author'

        date_tag = soup.find('div', {'class': 'caas-attr-time-style'})
        date = date_tag.find('time').get_text() if date_tag else 'No Date'

        body = soup.get_text()

        doc = Document()
        doc.add(Field('Title', str(title), metaType))
        doc.add(Field('Body', str(body), contextType))
        writer.addDocument(doc)
    writer.close()


def retrieve(storedir, query):
    print("paths.get = ", Paths.get(storedir))
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
            "title": doc.get("Title").replace('\n', '').replace('\t', ''),
            "text": body_text
        })

    return topkdocs

print("Indexing...")
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
create_index(index_dir, html_dir)

@app.before_first_request
def load_index():
    global index_handler
    index_handler = IndexHandler()

@app.route('/')
def root():
    return "Welcome to Yahoo Finance Search Engine API"


@app.route('/search/<query>', methods=['GET'])
def search(query):
    results = retrieve(index_dir, query)
    print(results)
    return jsonify(results)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
