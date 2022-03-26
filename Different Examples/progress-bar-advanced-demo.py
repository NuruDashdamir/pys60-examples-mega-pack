# -*- coding: utf-8 -*-
# by dimy44

import appuifw
import e32
from topwindow import TopWindow
from graphics import Image



class Pbar(object):


    def __init__(self):
        self.old_func_focus = appuifw.app.focus
        appuifw.app.focus = self.focus
        self.focusflag = 1
        if e32.s60_version_info >= (2, 8):
            self.scr = appuifw.app.layout(appuifw.EScreen)[0]
        else:
            self.scr = (176, 208)
        img_none = Image.new((1, 1))
        h = img_none.measure_text(u'by', 'annotation')[0]
        self.__h_text = h[3] - h[1]
        self.__dislocation_text = h[3]
        h2 = img_none.measure_text(u'by', 'dense')[0]
        h_text2 = h2[3] - h2[1]
        self.__dislocation_text2 = h2[3]
        self.__sizeW = 6 + h_text2
        self.__sizeY = self.__sizeW + self.__h_text * 2 + 6
        self.img = Image.new((self.scr[0] - 10, self.__sizeY))
        self.top_shadow = TopWindow()
        x = max(self.scr)
        self.top_shadow.position = (-x, -x)
        self.top_shadow.shadow = x / 2
        self.window = TopWindow()
        self.window.size = (self.scr[0] - 10, self.__sizeY)
        self.window.position = (5, self.scr[1] / 2 - self.__sizeY / 2)
        self.color_background = 0x555500
        self.color_text = 0xffffff
        self.color_background2 = 0xffffff
        self.color_text2 = 0x707070
        self.img1 = Image.new((self.scr[0] - 22, self.__sizeW), mode = 'RGB')
        self.img2 = Image.new((self.scr[0] - 22, self.__sizeW - 2), mode = 'RGB')
        self.img_gradient = Image.new((self.scr[0] - 22, self.__sizeW - 2), mode = 'RGB')
        r = 255 / ((self.scr[0] - 22) / 4.0)
        for i in xrange(self.scr[0] - 22):
            if i <= (self.scr[0] - 22) / 4.0:
                self.img_gradient.line((i, 0, i, self.__sizeW - 2), (255, int(i * r), 0))
            elif (self.scr[0] - 22) / 4.0 < i <= (self.scr[0] - 22) / 2.0:
                self.img_gradient.line((i, 0, i, self.__sizeW - 2), (int(255 - (i - (self.scr[0] - 22) / 4.0) * r), 255, 0))
            elif (self.scr[0] - 22) / 2.0 < i <= (self.scr[0] - 22) * 3 / 4.0:
                self.img_gradient.line((i, 0, i, self.__sizeW - 2), (0, 255, int((i - (self.scr[0] - 22) / 2.0) * r)))
            else:
                self.img_gradient.line((i, 0, i, self.__sizeW - 2), (0, int(255 - (i - (self.scr[0] - 22) * 3 /4.0) * r), 255))
        e32.ao_yield()


    def set_posY(self, pos):
        if not isinstance(pos, int): return
        pos = min(self.scr[1] - self.__sizeY, max(0, pos))
        self.window.position = (5, pos)
        

    position_y = property(lambda self: self.window.position[1], set_posY)


    size_y = property(lambda self: self.__sizeY)


    def x_text(self, text, font, w):
        xx = self.img.measure_text(text, font, maxwidth = w)
        if xx[2] < len(text):
            text = '%s%s' % (text[:xx[2] - 1], u'...')
            xx = self.img.measure_text(text, font)
        return  text, (self.scr[0] - xx[0][2]) / 2

    def show(self, goto, full, text=u'Loading...', shadow=1, stop=1):
        if goto > full or \
        not self.focusflag or \
        not full or \
        goto < 0:
            return
        if isinstance(text, (tuple, list)):
            text, text2 = text
        else: text2 = None
        text, xx = self.x_text(text, 'annotation', self.scr[0] - 26)
        xx -=5
        try:
            self.window.remove_image(self.img)
        except ValueError: pass
        self.img.rectangle((0, 0, self.img.size[0], self.__sizeY), 0xcccccc, self.color_background)
        x = abs((self.img.size[0] - 12) * goto / full)
        self.img1.clear(self.color_background2)
        a, b = self.img1.size
        self.img2.blit(self.img_gradient)
        if text2:
            text2, xx2 = self.x_text(text2, 'dense', self.scr[0] - 37)
            xx2 -= 11
            self.img1.text((xx2, b - 3 - self.__dislocation_text2), text2, self.color_text2, 'dense')
            self.img2.text((xx2, b - 4 - self.__dislocation_text2), text2, 0, 'dense')
        self.img1.blit(self.img2, source = (0, 0, x, self.__sizeW), target = (0, 1))
        self.img1.rectangle((0, 0, a, b), 0xcccccc)
        self.img.blit(self.img1, target = (6, self.__sizeY - self.__sizeW - 6))
        self.img.text((xx, self.__sizeY - self.__sizeW - 6 - self.__h_text / 2 - self.__dislocation_text), text, self.color_text, 'annotation')
        self.window.add_image(self.img, (0, 0))
        if shadow and not self.top_shadow.visible:
            self.top_shadow.show()
        self.window.show()
        e32.ao_yield()
        if goto == full and stop:
            e32.ao_sleep(0.1, self.stop)


    def stop(self):
        self.top_shadow.hide()
        self.window.hide()


    def focus(self, f):
        self.focusflag = f
        if not self.focusflag: self.stop()
        if self.old_func_focus:
            self.old_func_focus(self.focusflag)


#  example:
if __name__ == '__main__':

    bar = Pbar() # instance

    # необязательные аттрибуты:
    # position_y;
    # color_background;
    # color_text.
    # color_background2;
    # color_text2.

    # параметр size_y - размер окошка по оси Y, только для чтения.

    # метод show(goto, full [, text [, shadow [, stop]]]) - вывод окна на экран,
    # где  в аргументах: 
    # goto - текущее значение,
    # full - максимальное значение,
    # text - строка в юникоде, либо кортеж (список) из двух строк в юникоде,
    # shadow - выводить или не выводить тень (1 или 0),
    # stop - скрывать ли окно при достижении значения full (1 или 0).
    
    # метод stop() - скрывает окно.
    
    # в нашем примере выведем два прогрессбара:
    # важно: тень выводить только в прогрессбаре,
    # инстанс которого создан самым первым,
    #иначе тень второго накроет первого.
    bar2 = Pbar() # второй инстанс.
    bar2.color_background = 0x888800
    bar2.color_text = 0xffff66
    bar2.color_background2 = 0x999999
    bar2.color_text2 = 0xffffff
    bar2.position_y = bar.position_y + bar.size_y # поместили второй под первым.

    for x in xrange(3): # 3 прохода (0,1,2).
        for i in xrange(151): # full = 150
            text = ('bar: грузится %d из 3'.decode('utf-8') % (x + 1), u'Total: %d%%' % ((i + x * 150) / 450.0 * 100))
            bar.show(x * 150 +  i, 3 * 150, text)
            text2 = (u'bar2: %d / 150' % i, u'Loading %d%%' % (i / 150.0 * 100))
            bar2.show(i, 150, text2, shadow = 0, stop = 0) # stop = 0, чтоб не скрывать и сразу заново выводить после 1го и 2го проходов.
            e32.ao_sleep(0.001)
    bar2.stop() # раз был задан stop = 0, то сейчас, после отработки, надо скрыть.

    print 'Finish!' # :)

