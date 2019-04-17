
def load_dictionary(filename):
    f = file(filename, "r")
    dict = {}
    for line in f:
        key, value = line.split(":")
        dict[key.strip()] = value.strip()
    f.close()
    return dict
