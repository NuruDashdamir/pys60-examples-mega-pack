import urllib

def get_text_from_url(address):
    return urllib.urlopen(address).read()

url_address = "http://google.com"
data_from_url = get_text_from_url(url_address)

# don't print whole string, it causes bugs, print is only for debugging 
print(data_from_url[:128])
