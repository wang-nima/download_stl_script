import requests
import json


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

    #get access code
    client_id = "59aedb83c379fbc8652f"
    client_secret = "fa4be59ba7faeba5bb0cd527c568b8e7"
    redirect_uri = "http://wang-nima.github.io"
    #url = "https://www.thingiverse.com/login/oauth/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri
    
    #payload = {'client_id': client_id, 'redirect_uri': redirect_uri}
    #r = requests.get("https://www.thingiverse.com/login/oauth/authorize", params=payload)
    #print r.url
    
    #test url
    #url = "https://api.weibo.com/2/statuses/public_timeline.json?access_token=2.00I_rGZF0xiu8g142bd2f6a5jwh7vD"
    
    #code = "d1e0036de21bcc8d28a52a20a80ae763"
    #
    ## get token
    #url = "https://www.thingiverse.com/login/oauth/access_token?" + "client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&client_secret=" + client_secret + "&code=" + code
    #
    #r = requests.post(url)
    #
    #print r.text
    
    token = "08a7a99f93bc5c15e5ddb0f737256a9d"
    arg = {'access_token': token}

    print "Please enter your query:"
    item = raw_input('>> ')

    r = requests.get("https://api.thingiverse.com/search/" + item, params=arg)

    #print r

    if r.status_code == 401:
        print "token expire"
        return
    elif r.status_code == 404:
        print "item not found"
        return

    things_json = r.json()

    #print requests.get("https://api.thingiverse.com/search/" + item, params=arg).text

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
    
    r = requests.get("https://api.thingiverse.com/things/" + thing_selected_id + "/files", params=arg)
    thing_file_json = r.json()

    idx = 0
    for i in thing_file_json:
        idx += 1
        print str(idx)+")", i["name"]

    print "Please select STL file to download:"
    index = int(raw_input('>> '))
    download_link = thing_file_json[index-1]["public_url"]
    file_name = thing_file_json[index-1]["name"]


    print "Downloading " + file_name
    download_file(download_link, file_name)
    print thing_file_json[index-1]["formatted_size"]+ " downloaded"
    return

if __name__ == "__main__":
    main();
