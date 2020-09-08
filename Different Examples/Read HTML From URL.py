import urllib


def getDataFromURL(urlAdress):
    code = urllib.urlopen(URL).read()
    return code

print("Downloading")
URL = "http://google.com"
dataFromUrl = getDataFromURL(URL)
print("Downloaded!")
print(dataFromUrl)

