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


app = Flask(__name__)
@app.route('/')
def callback():
    code = request.args.get('code')
    get_token(code)

def get_token(code):
    #print code
    args = {'client_id': CLIENT_ID, 'redirect_uri': REDIRECT_URI, 'client_secret': CLIENT_SECRET, 'code':code}
    r = requests.post("https://www.thingiverse.com/login/oauth/access_token", params=args)
    form = r.text
    token = form.split('&')[0]
    token = token.split('=')[1]
    file_object = open("key.txt", 'w')
    token = file_object.write(token)
    file_object.close()
    print "we have new valid token in key.txt now!"

class server_thread(threading.Thread):
    def run(self):
        app.run(port=54321)

def main():
    server_thd = server_thread()
    server_thd.start()
    args = {'client_id': CLIENT_ID, 'redirect_uri': REDIRECT_URI}
    r = requests.get("https://www.thingiverse.com/login/oauth/authorize", params=args)
    webbrowser.open_new(r.url)

if __name__ == "__main__":
    main()
