import urllib

def get_data_from_url(address):
    return urllib.urlopen(address).read()

print("Downloading")
url_address = "http://google.com"
data_from_url = get_data_from_url(url_address)
print("Downloaded!")
print(data_from_url[:128])
# DO NOT PRINT WHOLE STRING, IT CAUSES BUGS
# PRINT IS ONLY FOR DEBUGGING
