# app.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
SOLR_URL = "http://localhost:8983/solr/solr_java_books/query"

@app.route('/', methods=['GET', 'POST'])
def index():
    books = []
    if request.method == 'POST':
        search_term = request.form.get('search', '')
        print(search_term)
        query_params = {
            'q': f'author:"{search_term}" OR title:{search_term} OR published:{search_term} OR category{search_term}',
            'q.op': 'OR',
            
        }
        # print(query_params)
        response = requests.get(SOLR_URL, params=query_params)
        # print(response.json())
        if response.status_code == 200:
            data = response.json()
            # print(data.get('response', {}).get('docs', []))
            books = data.get('response', {}).get('docs', [])
    
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)