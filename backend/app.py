import os
from flask import Flask, jsonify
from flask_cors import CORS
import lucene
from org.apache.lucene.store import SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher
import json

app = Flask(__name__)
CORS(app)

index_dir = os.path.join(os.getcwd(), 'index')

os.chdir("../")

json_location = os.path.join(os.getcwd(), 'crawler', 'output.json')

os.chdir(os.path.join(os.getcwd(), 'backend'))

def create_index(dir):
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

    if not os.path.exists(json_location):
        print(f"File not found: {json_location}")
    else:
        with open(json_location, 'r') as f:
            try:
                content = f.read()
                data = json.loads(content)
                for obj in data:
                    doc = Document()
                    doc.add(Field('Title', str(obj['title']), contextType))
                    doc.add(Field('Link', str(obj['link']), metaType))
                    doc.add(Field('Author', str(obj['author']), metaType))
                    doc.add(Field('Date', str(obj['date']), metaType))
                    doc.add(Field('Body', str(obj['content']), contextType))
                    writer.addDocument(doc)
                writer.close()
                print("JSON data loaded successfully.")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")


def retrieve(storedir, query):
    vm_env = lucene.getVMEnv()
    if vm_env is not None:
        vm_env.attachCurrentThread()

    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    parser = QueryParser('Body', StandardAnalyzer())

    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 20).scoreDocs

    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        body_text = doc.get("Body").strip().replace('\n', '')
        body_text = " ".join(body_text.split())

        topkdocs.append({
            "score": hit.score,
            "title": doc.get("Title").replace('\n', '').replace('\t', ''),
            "text": body_text,
            "link": doc.get("Link"),
            "author": doc.get("Author"),
            "date": doc.get("Date")
        })

    return topkdocs

print("Indexing...")
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
create_index(index_dir)

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
