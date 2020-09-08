# icon_image.py
# called by just import icon_image
# im = icon_image(file_mbm, idx)
from graphics import Image
from struct import unpack

def readL(f, pos=None):
    if pos is not None:
        f.seek(pos)
    return unpack('L', f.read(4))[0]

def open(file_mbm='z:\\system\\data\\avkon.mbm', idx = 28):

    # read icon data from mbm file
    f = file(file_mbm, 'rb')
    if readL(f) != 0x10000041:
        return None  # work for mbm on ROM (z:) only
    start = readL(f, 8+4*idx)
    f.seek(start+20)
    length = readL(f) - readL(f)  # pd_size - offset
    width, height = readL(f), readL(f)
    enc = readL(f, start+56)
    f.seek(start+68)
    data_encoded = f.read(length)

    # decode the data
    data_padded = rle_decode(data_encoded, enc)
    mat = bit_matrix(data_padded, width, height)
    
    im = Image.new((width, height), '1')
    for j in range(height):
        for i in range(width):
            im.point((i,j), mat[j][i]*0xffffff)
    return im

# Decode of 8-bit RLE
# Either to repeat-(n+1)-times or not repeat (100-n) bytes
def rle_decode(bytes, enc=1):
    if not enc: return bytes
    out = []
    i = 0
    while i < len(bytes):
        n = ord(bytes[i])
        i += 1
        if n < 0x80:
            out.append( bytes[i] * (n+1) )
            i += 1
        else:
            n = 0x100 - n
            out.append( bytes[i:i+n] )
            i += n
    return ''.join(out)

# from bytes to bit matrix
# Each line was padded to 4-byte boundary, must discard the end
def bit_matrix(bytes, width, height):
    mat = []
    k = 0
    for j in range(height):
        line = []
        while len(line)<width:
            longint, = unpack('L', bytes[k: k+4])
            k += 4
            toget = min(width - len(line), 32)
            for i in range(toget):
                longint, r = divmod(longint, 2)
                line.append(int(r))
        mat.append(line)
    return mat
