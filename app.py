import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.js')

# Path to the folder containing HTML files
HTML_FOLDER = os.path.join(os.getcwd(), 'html_Pages')

# list all files in the HTML_FOLDER
@app.route('/pages', methods=['GET'])
def get_html_pages():
    try:
        files = [f for f in os.listdir(HTML_FOLDER) if os.path.isfile(os.path.join(HTML_FOLDER, f)) and f.endswith('.html')]
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Search with query
@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query', '')
    # query = "nomura"

    matching_files = []
    
    # iterate through the HTML_FOLDER
    for filename in os.listdir(HTML_FOLDER):
        if filename.endswith('.html'):
            filepath = os.path.join(HTML_FOLDER, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                # check for query in file content
                if query.lower() in content.lower():
                    matching_files.append(filename)
                    
    return jsonify(matching_files)
  
if __name__ == "__main__":
    app.run(debug=True)