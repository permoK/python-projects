from xata.client import XataClient
xata = XataClient()

data = xata.data().search_branch({
    "query": "",
    "tables": [
        {
            "table": "tag"
        },
           ],
    "fuzziness": 0,
    "prefix": "phrase"
})

records = data['records']


for record in records:
    record_id = record['id']
    record_name = record['name']
    record_xata_data = record['xata']

    print("Record ID: ", record_id)
    print("Record Name: ", record_name)
    print("Xata Data: ", record_xata_data, "\n")
               

