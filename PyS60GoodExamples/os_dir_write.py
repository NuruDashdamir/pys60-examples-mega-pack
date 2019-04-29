# this script lets you write a file into a directory



# drefine the directory and file name to write the file into
imagedir=u'c:\\witetest.txt'

# create the file
file = open(imagedir,'w')

# write some text into it
file.write('hello, this works')

# close the file
file.close()

print "file stored"
