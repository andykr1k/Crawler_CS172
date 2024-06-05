import os
from flask import Flask, request

from pylucene_indexer import retrieve

app = Flask(__name__)

@app.route('/', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    
    storedir = os.path.join(os.getcwd(), 'pylucene_index')
    
    retrieve(storedir, query)
  
if __name__ == "__main__":
    app.run(debug=True)