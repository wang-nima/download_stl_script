#!/usr/bin/env python
import requests
import json
import webbrowser
from flask import Flask, abort, request

CLIENT_ID = "59aedb83c379fbc8652f"
CLIENT_SECRET = "fa4be59ba7faeba5bb0cd527c568b8e7"
REDIRECT_URI = "http://localhost:54321"

def download_file(url, file_name):
    local_filename = file_name
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()


def pop_up_broswer():
    args = {'client_id': CLIENT_ID, 'redirect_uri': REDIRECT_URI}
    r = requests.get("https://www.thingiverse.com/login/oauth/authorize", params=args)
    print r.url

app = Flask(__name__)
@app.route('/')
def callback():
    code = request.args.get('code')
    access_token = get_token(code)

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]

def query():

    # read access token from file
    file_object = open("key.txt", 'r')
    try:
        token = file_object.read(32)
    finally:
        file_object.close()

    args = {'access_token': token}

    print "Please enter your query:"
    item = raw_input('>> ')

    r = requests.get("https://api.thingiverse.com/search/" + item, params=args)

    if r.status_code == 401:
        print "token expire"
        pop_up_broswer()
        return
    elif r.status_code == 404:
        print "item not found"
        return

    things_json = r.json()
    idx = 0
    for i in things_json:
        idx += 1
        print str(idx)+")", i["name"]

    print "Please choose one object:"
    index = int(raw_input('>> '))
    if index <= 0 or index > idx:
        print "invalid index"
        return
        
    thing_selected = things_json[index-1]
    thing_selected_id = thing_selected["id"]
    
    r = requests.get("https://api.thingiverse.com/things/" + thing_selected_id + "/files", params=args)
    thing_file_json = r.json()

    idx = 0
    for i in thing_file_json:
        idx += 1
        print str(idx)+")", i["name"]


    print "Please select STL file to download:"
    index = int(raw_input('>> '))
    if index <= 0 or index > idx:
        print "invalid index"
        return

    download_link = thing_file_json[index-1]["public_url"]
    file_name = thing_file_json[index-1]["name"]
    print "Downloading " + file_name
    download_file(download_link, file_name)
    print thing_file_json[index-1]["formatted_size"]+ " downloaded"

    return

if __name__ == "__main__":
    app.run(debug=True, port=54321)
