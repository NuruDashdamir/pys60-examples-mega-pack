# графический рисунок
# использование всех клавишь курсора: верх,вниз,лево,право, для перемещения точки

import appuifw
from appuifw import *
import e32
from key_codes import *
# включаем graohics чтобы вложить материал
from graphics import *


class Keyboard(object):
    def __init__(self,onevent=lambda:None):
        self._keyboard_state={}
        self._downs={}
        self._onevent=onevent
    def handle_event(self,event):
        if event['type'] == appuifw.EEventKeyDown:
            code=event['scancode']
            if not self.is_down(code):
                self._downs[code]=self._downs.get(code,0)+1
            self._keyboard_state[code]=1
        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']]=0
        self._onevent()
    def is_down(self,scancode):
        return self._keyboard_state.get(scancode,0)
    def pressed(self,scancode):
        if self._downs.get(scancode,0):
            self._downs[scancode]-=1
            return True
        return False

keyboard=Keyboard()



def quit():
    global running
    running=0
    appuifw.app.set_exit()


appuifw.app.screen='full'
# создаем пустое изображение, которое появляется как белое
img=Image.new((176,208))
# определение blobsize и начальных координат (x,y) точки на холсте
blobsize=30
location_x = 100.
location_y = 100.

# определении функции которая изменит экран, в этом случае он должен быть
# оттянутый снова и снова (используют для этого функцию  .blit)
def handle_redraw(rect):
    canvas.blit(img)

running=1

# определение холста и активация функции измены как отзыв, а также ключевой функции просмотра (keyboard.handle_event)
canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=handle_redraw)
# установка прикладного тела как холст
appuifw.app.body=canvas

app.exit_key_handler=quit

# определение цикла, чтобы создать базу которая будет появлятся снова и снова  
while running:
    # очистить изображение (помещеное как белое изображение)
    img.clear(0x555555)
    # назначение точки и добавление это к изображению, определение: x,y координат потока, а также ее цвет и размер
    img.point((location_x + blobsize/2,location_y + blobsize/2),0x009999,width=blobsize)
    # изменить изображение
    handle_redraw(())
    # это нужно чтобы начать короткого планировщика, который проверяет ключевые события
    e32.ao_yield()
    # если нажимать клавишу курсора, будет изменятся координата х на 1 параметр точки
    if keyboard.is_down(EScancodeLeftArrow):
        location_x = location_x - 1

    if keyboard.is_down(EScancodeRightArrow):
        location_x = location_x + 1

    # нажимаем в низ и координата y  изменяется на 1 параметр точки
    if keyboard.is_down(EScancodeDownArrow):
        location_y = location_y + 1


    if keyboard.is_down(EScancodeUpArrow):
        location_y = location_y - 1






        


 



