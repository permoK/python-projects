# hello_algolia.py
from algoliasearch.search_client import SearchClient

# Connect and authenticate with your Algolia app
client = SearchClient.create("5AM91AHDV1", "ff4bdb7ea8967af46003787e66cfd6f3")

# Create a new index and add a record
index = client.init_index("notes_files")

# Search the index and print the results
results = index.search("deep")
print(results["hits"][0])

