#!/usr/bin/env python
import requests
import json
import webbrowser
import threading
import time
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

def main():

    # read access token from file
    file_object = open("key.txt", 'r')
    token = file_object.read(32)
    file_object.close()

    args = {'access_token': token}

    print "Please enter your query:"
    item = raw_input('>> ')

    r = requests.get("https://api.thingiverse.com/search/" + item, params=args)

    if r.status_code == 401:
        print "token expire"
        token = get_new_token()
    elif r.status_code == 404:
        print "item not found"

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
    main()
