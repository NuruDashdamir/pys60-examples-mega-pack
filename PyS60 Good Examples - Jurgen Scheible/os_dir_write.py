# this script lets you write a file into a directory
# drefine the directory and file name to write the file into

file_to_write = u'e:\\writetest.txt'

# create the file
file = open(file_to_write, 'w')

# write some text into it
file.write('Hello! This works!')

# close the file
file.close()

# debug print
print 'File saved!'
