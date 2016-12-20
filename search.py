import json, sys
from apiclient.discovery import build

def search(search_term):
    search_engine_id = '010780822262881999248:0j5wzz3i4xc'
    api_key = 'AIzaSyCvHK6q0itCAxq8CaVnQIOF-mnVBd6D6vA'

    service = build('customsearch', 'v1', developerKey=api_key)

    collection = service.cse()

    # search_term = "pizza"

    # Make an HTTP request object
    request = collection.list(q=search_term, num=10, start=1, cx=search_engine_id)

    response = request.execute()

    with open('results.json', 'w') as outfile:
        json.dump(response, outfile, sort_keys = True, indent = 2, ensure_ascii=True)
		
	return response

if __name__ == "__main__":
    search("justin timberlake")
    with open('results.json') as data_file:
        data = json.load(data_file)

    """nu stiu cum sa fac sa iau raspunsul cel mai bun, imi da 10 rezultate, dar nu sunt toate tocmai bune, depinde de ce gaseste"""
    ind = 0 # intre 0 si 9
    print(data['items'][ind]['snippet'])


