from flask import Flask, request, jsonify, render_template

# search for the data in algolia index
from algoliasearch.search_client import SearchClient

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def data():
    # Get the data from the form
    form_data = request.form['q']
    print(form_data)


    # Connect and authenticate with your Algolia app
    client = SearchClient.create("5AM91AHDV1", "ff4bdb7ea8967af46003787e66cfd6f3")

    # Create a new index and add a record
    index = client.init_index("notes_files")

    # Search the index and print the results
    results = index.search(form_data)
    records = results['hits']
    # print(len(results['hits'])
    # print(results['hits'][0]['noteTitle'])
    print(records[0])
    # for record in records:
    #     print(records['noteTitle'])

    return render_template('data.html', results=records)


if __name__ == '__main__':
    app.run(debug=True)
