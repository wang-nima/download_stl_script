import requests

#get access code
client_id = "59aedb83c379fbc8652f"
redirect_uri = "http://wang-nima.github.io"
url = "https://www.thingiverse.com/login/oauth/authorize?client_id=" + client_id + "&redirect_uri=" + redirect_uri

r = requests.get(url)

#res_data = urllib2.urlopen(request)
#res = res_data.read()

print r.url
