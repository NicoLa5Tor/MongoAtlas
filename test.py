import requests
import json
url = 'https://mongoatlas-crxv.onrender.com'
try:
    uri = f'{url}/update_item'
    data = {
    'name_db' : 'NicolasJuan',   
    'name_collection' : 'Content',
    'item' : 'cosas',
    '_id' : 'nuevoitem'
    }
    response = requests.put(url=uri,json=data)
    print(response.json())
 
except Exception as e:
    print(e)