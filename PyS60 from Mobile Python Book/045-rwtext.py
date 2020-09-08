
def save_list(filename, list):
    f = file(filename, "w")
    for item in list:
        print >> f, item
    f.close()

def load_list(filename):
    f = file(filename, "r")
    lst = []
    for line in f:
        lst.append(line.strip())
    f.close()
    return lst

test_list = ["first line", "second line", "that's all"]
save_list(u"c:\\python\\test.txt", test_list)
print load_list(u"c:\\python\\test.txt")
