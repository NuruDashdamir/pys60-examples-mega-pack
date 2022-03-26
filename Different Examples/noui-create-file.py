# this script lets you write a file to drive

# drefine the directory and file name to write the file into
imageLocation=u'D:\\writetest.txt'

# create the file
file = open(imageLocation,'w')

# write some text into it
file.write('Hello, this works!')

# close the file
file.close()

print("file stored")
