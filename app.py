from flask import Flask, render_template, request
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import os
import requests
from bs4 import BeautifulSoup
from threaded_crawler import crawl_and_index  # Import your advanced crawling function

app = Flask(__name__)

# Create an index directory if it doesn't exist
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

# Define the schema for indexing
schema = Schema(title=TEXT(stored=True), content=TEXT)
ix = create_in("indexdir", schema)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query_str = request.form['query']
    results = []

    # Search logic
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        # Actual search logic could involve more complex ranking algorithms
        results = searcher.search(query)

    return render_template('index.html', results=results, query=query_str)

if __name__ == '__main__':
    # Example URL to crawl and index (You can replace this or make it dynamic)
    crawl_and_index("http://example.com")  # Trigger the crawling process on startup
    app.run(debug=True, host='0.0.0.0', port=5000)
