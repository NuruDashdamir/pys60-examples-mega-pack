
def init_server():
    global phone_req, cache
    phone_req = {}
    cache = {}

def process_json(msg):
    global cache
    cache = msg
    return phone_req

def process_get(path, query):
    phone_req[path] = True
    if path in cache:
        return cache[path]
    return "text/plain",\
           "Your request is being processed."\
           "Reload the page after a while."

init_server()
httpd = Server(('', 9000), Handler)
httpd.serve_forever()
