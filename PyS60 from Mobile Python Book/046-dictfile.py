
def save_dictionary(filename, dict):
    f = file(filename, "w")
    for key, value in dict.items():
        print >> f, "%s: %s" % (key, value)
    f.close()
