import appuifw
import e32
import os
import zipfile
from appuifw import *
from graphics import *

def new():
    global aktiv
    global name
    i = popup_menu([u'zip'])
    if (i == 0):
        txt = 'zip'
    if (i == 1):
        txt = 'srz'
    try:
        (aktiv, name,) = (['new',
          txt],
         query(ru('Ar\xc5\x9fiv ismi'), 'text', ru(('Dj_turan.' + txt))))
        if (len(name) > 4):
            name = codos(name)
            if (os.path.exists((zdir + name)) == 1):
                note(ru('Ayn\xc4\xb1 isimde ar\xc5\x9fiv dosyas\xc4\xb1 zaten mevcut'), 'error')
                new()
            elif (i == 0):
                spisok()
            else:
                sborka()
    except:
        None



def opens():
    global p
    global d
    global f
    global i
    global rsf
    global z
    global dir
    n = f[(p + d)]
    if (zipfile.is_zipfile((zdir + n)) == 1):
        z = zipfile.ZipFile((zdir + n), 'r', com)
        (f, p, i, d, dir, rsf,) = (z.namelist(),
         0,
         0,
         0,
         '',
         ru('Geri'))

        def one():
            global sp
            global aktiv
            sp = [f[(p + d)]]
            aktiv = ['open',
             'one']
            fileman()



        def all():
            global sp
            global aktiv
            sp = f
            aktiv = ['open',
             'all']
            fileman()


        app.menu = [(ru('\xc3\x87\xc4\xb1kart'),
          one),
         (ru('T\xc3\xbcm\xc3\xbcn\xc3\xbc \xc3\xa7\xc4\xb1kart'),
          all)]
        canvas.bind(8, non)

        def tmn():
            z.close()
            main()


        app.exit_key_handler = tmn



def spisok():
    global p
    global d
    global f
    global i
    global rsf
    global dir
    (dir, p, i, d, rsf,) = ('',
     0,
     0,
     0,
     ru('Geri'))
    if (aktiv[1] == 'zip'):
        f = usp
    else:
        f = sp
    if (len(usp) > 0):
        app.menu = [(ru('Ekle'),
          fileman),
         (ru('Ar\xc5\x9fivle'),
          compress)]
    else:
        app.menu = [(ru('Ekle'),
          fileman)]
    canvas.bind(63496, non)
    canvas.bind(63495, non)
    canvas.bind(8, delit)
    app.exit_key_handler = main



def sborka():

    def sbr(inf):
        inf = codos(inf)
        F = open('e:/system/apps/zippy/info.txt', 'w')
        F.write(inf)
        F.close()
        vbr()



    def cmnt(inf):
        inf += ('\r\n' + txt.get())
        app.body = canvas
        txt.set(u'')
        sbr(inf)



    def vbr():
        global sdir
        i = popup_menu([ru('Buraya kaydet'),
         ru('\xc5\x9ee\xc3\xa7ilmedi')])
        if (i == 0):
            sdir = ''
            spisok()
        elif (i == 1):
            sdir = '!'
            spisok()
        else:
            main()


    inf = query(ru('Ar\xc5\x9fiv ismi'), 'text')
    if (inf == None):
        vbr()
    else:
        if (query(ru('Eklenemiyor yeniden a\xc3\xa7\xc4\xb1l\xc4\xb1yor'), 'query') == True):
            inf += '\r\nrestart'
        if (query(ru('A\xc3\xa7\xc4\xb1klama ekle'), 'query') == True):
            app.body = txt
            app.menu = [(ru('Kaydet'),
              lambda :cmnt(inf)
)]
            app.exit_key_handler = lambda :cmnt(inf)

        else:
            sbr(inf)



def fileman():
    global i
    global p
    global d
    global dir
    global f
    (dir, f, p, i, d,) = ('',
     ['c:',
      'e:'],
     0,
     0,
     0)
    if (aktiv[0] == 'new'):
        app.menu = [(ru('Ar\xc5\x9fivleme listesi'),
          spisok)]
        canvas.bind(63557, skan)
    else:
        app.menu = []
        canvas.bind(63557, decompress)
    canvas.bind(63496, go)
    canvas.bind(63495, back)
    canvas.bind(8, non)
    app.exit_key_handler = main



def skan():
    global sp
    global run
    global usp
    F = f[(p + d)]
    if (os.path.isfile((dir + F)) == 1):
        sp.append((dir + F))
        usp.append(F)
    else:
        efile = os.listdir(((dir + F) + '/'))
        (run, e, i, l, a, ua,) = (0,
         0,
         0,
         len(dir),
         [],
         [])
        while (len(efile) > e):
            a.append((((dir + F) + '/') + efile[e]))
            ua.append(((F + '/') + efile[e]))
            e += 1

        while (len(a) > i):
            if (os.path.isdir(a[i]) == 1):
                try:
                    (c, q,) = (os.listdir(a[i]),
                     0)
                    while (len(c) > q):
                        aa = ((a[i] + '/') + c[q])
                        a[((i + 1) + q):((i + 1) + q)] = [aa]
                        ua[((i + 1) + q):((i + 1) + q)] = [aa[l:]]
                        q += 1

                    del a[i:(i + 1)]
                    del ua[i:(i + 1)]
                except:
                    del a[i:(i + 1)]
                    del ua[i:(i + 1)]
            else:
                i += 1
        else:
            (run, sp, usp,) = (1,
             (sp + a),
             (usp + ua))




def compress():
    global run
    (obw, per, run,) = (len(sp),
     0,
     0)
    z = zipfile.ZipFile((zdir + name), 'w', com)
    if (aktiv[1] == 'srz'):
        try:
            z.write('e:/system/apps/zippy/info.txt', 'info/info.txt')
        except:
            None
    img.rectangle((20,
     120,
     156,
     140), 7829488, width=20)
    img.text((50,
     122), ru('Ar\xc5\x9fivleniyor . . .'), font=u'apl')
    while (obw > per):
        img.rectangle((18,
         132,
         (18 + ((140 * per) / obw)),
         137), 255, width=10)
        try:
            if (aktiv[1] == 'zip'):
                z.write(sp[per], usp[per])
            elif (sdir == ''):
                z.write(sp[per], (sp[per][0] + sp[per][2:]))
            else:
                z.write(sp[per], (sdir + sp[per][2:]))
            per += 1
        except:
            per += 1
        redraw(())
        e32.ao_yield()

    z.close()
    run = 1
    main()



def decompress():
    global run
    (obw, per, run,) = (len(sp),
     0,
     0)
    try:
        di = ((dir + f[(p + d)]) + '/')
    except:
        di = dir
    img.rectangle((20,
     120,
     156,
     140), 7829488, width=20)
    img.text((50,
     122), ru('\xc3\x87\xc4\xb1kart\xc4\xb1l\xc4\xb1yor . . .'), font=u'apl')
    while (obw > per):
        img.rectangle((18,
         132,
         (18 + ((140 * per) / obw)),
         137), 255, width=10)
        try:
            try:
                F = open((di + sp[per]), 'w')
            except:
                os.makedirs((di + os.path.dirname(sp[per])))
                F = open((di + sp[per]), 'w')
            F.write(z.read(sp[per]))
            F.close()
        except:
            None
        per += 1
        redraw(())
        e32.ao_yield()

    z.close()
    run = 1
    main()



def about():
    f = open('e:/system/apps/zippy/about.txt')
    text = f.read()
    f.close()
    app.body = txt
    txt.set(ru(text))
    txt.set_pos(0)

    def cls():
        app.body = canvas
        txt.set(u'')
        main()


    app.menu = []
    app.exit_key_handler = cls



def newname():
    n = f[(p + d)]
    newnam = query(ru('Yeni isim'), 'text', ru(n))
    try:
        os.rename((zdir + n), ((zdir + '/') + codos(newnam)))
        main()
    except:
        None



def delzip():
    try:
        n = f[(p + d)]
        if (query((ru('Silisin mi?\n') + ru(n)), 'query') == True):
            os.remove((zdir + n))
            main()
        else:
            None
    except:
        None



def delit():
    n = (p + d)
    sp[n:(n + 1)] = []
    usp[n:(n + 1)] = []
    spisok()



def ru(x):
    t = x.decode('utf-8')
    return t



def codos(x):
    t = x.encode('utf-8')
    return t



def ris(i):
    if (len((dir + f[(i + d)])) == 2):
        img.rectangle((5,
         (17 + (12 * i)),
         13,
         (23 + (12 * i))), 10526880, width=5)
        img.rectangle((3,
         (14 + (12 * i)),
         15,
         (25 + (12 * i))), 5263440)
    elif (os.path.isdir((dir + f[(i + d)])) == 1):
        img.rectangle((3,
         (17 + (12 * i)),
         15,
         (25 + (12 * i))), 8421504)
        img.rectangle((3,
         (15 + (12 * i)),
         9,
         (20 + (12 * i))), 8421504)
        img.rectangle((5,
         (19 + (12 * i)),
         13,
         (23 + (12 * i))), 16776960, width=3)
        img.rectangle((4,
         (16 + (12 * i)),
         7,
         (19 + (12 * i))), 16776960, width=2)
    else:
        img.rectangle((5,
         (17 + (12 * i)),
         13,
         (23 + (12 * i))), 13684944, width=5)
        img.rectangle((3,
         (14 + (12 * i)),
         15,
         (25 + (12 * i))), 8421504)



def sort(s):
    (i, f, d,) = (0,
     [],
     [])
    while (len(s) > i):
        if (os.path.isdir((dir + s[i])) == 1):
            d.append(s[i])
            i += 1
        else:
            f.append(s[i])
            i += 1

    if (aktiv[0] == 'new'):
        return (d + f)
    else:
        return d



def up():
    global p
    global d
    if (p > 0):
        p -= 1
    elif (d > 0):
        d -= 1
    elif (len(f) > 14):
        (p, d,) = (14,
         (len(f) - 15))
    elif (len(f) > 0):
        p = (len(f) - 1)



def down():
    global p
    global d
    if (len(f) > 14):
        if (p < 14):
            p += 1
        elif (((p + d) + 1) < len(f)):
            d += 1
        else:
            (p, d,) = (0,
             0)
    elif (len(f) > 0):
        if ((p + 1) < len(f)):
            p += 1
        else:
            (p, d,) = (0,
             0)



def go():
    global i
    global p
    global d
    global dir
    global f
    if (len(f) > 0):
        if (os.path.isdir((dir + f[(p + d)])) == 1):
            dir += (f[(p + d)] + '/')
            f = os.listdir(dir)
            f = sort(f)
            (p, i, d,) = (0,
             0,
             0)



def back():
    global i
    global p
    global d
    global dir
    global f
    if (len(dir) > 3):
        z = os.path.dirname(dir)
        w = os.path.split(z)[1]
        z = os.path.dirname(z)
        if (len(z) > 3):
            dir = (z + '/')
        else:
            dir = z
        f = os.listdir(dir)
        f = sort(f)
        (p, i, d,) = (0,
         0,
         0)
        while (len(f) > p):
            if (f[p] == w):
                break
            else:
                p += 1

        if (p > 14):
            (d, p,) = ((p - 14),
             14)
    else:
        (dir, f, p, i, d,) = ('',
         ['c:',
          'e:'],
         0,
         0,
         0)



def main():
    global p
    global usp
    global d
    global f
    global i
    global rsf
    global sp
    global dir
    f = os.listdir(zdir)
    (dir, p, i, d, sp, usp, rsf,) = (zdir,
     0,
     0,
     0,
     [],
     [],
     ru('\xc3\x87\xc4\xb1k\xc4\xb1\xc5\x9f'))
    app.menu = [(ru('Yeni ar\xc5\x9fiv'),
      new),
     (ru('\xc4\xb0smi d\xc3\xbczelt'),
      newname)]
    try:
        os.remove('e:/system/apps/zippy/info.txt')
    except:
        None
    canvas.bind(63496, non)
    canvas.bind(63495, non)
    canvas.bind(8, delzip)
    canvas.bind(63557, opens)
    app.exit_key_handler = exit



def non():
    None



def exit():
    app.set_exit()


app.screen = 'full'
img = Image.new((176,
 208))

def redraw(rect):
    canvas.blit(img)


canvas = appuifw.Canvas(event_callback=None, redraw_callback=redraw)
app.body = canvas
canvas.bind(63497, up)
canvas.bind(63498, down)
txt = Text()
(txt.color, txt.font,) = (0,
 u'alp13')
txt.add(u'')
(zdir, com, run,) = ('e:/zipman/',
 zipfile.ZIP_DEFLATED,
 1)
if (os.path.exists('e:/zipman') == 0):
    os.mkdir('e:/Zipman')
main()
while run:
    img.clear(15790304)
    img.line((0,
     13,
     176,
     13), 8421504)
    img.line((0,
     194,
     176,
     194), 8421504)
    try:
        img.text((2,
         11), ru((dir + f[(p + d)])), fill=3158064, font=u'apl')
    except:
        img.text((2,
         11), ru(dir), fill=3158064, font=u'apl')
    img.text((5,
     206), ru('Men\xc3\xbc'), fill=3158064, font=u'apl')
    img.text((130,
     206), rsf, fill=3158064, font=u'apl')
    img.rectangle((0,
     (15 + (12 * p)),
     208,
     (23 + (12 * p))), 3158271, width=6)
    while (i < 15):
        try:
            img.text((20,
             (24 + (12 * i))), ru(f[(i + d)]), fill=3158064, font=u'apl')
            ris(i)
            i += 1
        except:
            break

    if (len(f) > 15):
        i -= 15
    else:
        i -= len(f)
    redraw(())
    e32.ao_yield()


