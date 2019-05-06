# ############################ #
# Написано AUN2000  для http://dimonvideo.ru
# ############################ #
# набрано в Notepad++
# http://notepad-plus.sourceforge.net/ru/site.htm
# кодировка UTF-8 без BOM                 
# ############################ #
# отлажено на Nokia E61 c  Python V1.3.22 
# не требующим подписи (selfsigned)
# ############################ #

import appuifw
import time
import e32
import graphics

global old_body, My_Text, list_Listbox_Type, My_Canvas, My_img,My_img_pattern, My_outline, My_width, My_fill

My_Text = appuifw.Text()

def ru(x):return x.decode('utf-8')
# перевод строки, набранной в UTF-8 в юникод

# ====   Секция основных средств UI    ========= #
def List_Demo():
	return[u'cakewalk', u'com-port', u'computer', u'bluetooth', u'mobile', u'screen', u'keys',u'aun2000']
# формированите списка, для демонстрации работы со списками.
	
def multi_query():
# appuifw.multi_query(label_1,label_2)
# два последовательно открывающихся окна для ввода строк
	T1,T2=appuifw.multi_query(ru('ВВОД СТРОКИ label_1'),ru('ВВОД СТРОКИ label_2')) 
	print u'multi_query'
	print u'label_1=',T1
	print u'label_2=',T2
 
def note_info():
# appuifw.note(text[,'info'[,global]])
# вывод окна сообщений (время около 3 секунд) 
# при global=1  сообщение выводится из фоного режима для программы, когда
# она свернута (не видима на экране)
	appuifw.note(ru('в type значение info'),'info')

# при сворачивании программы в фон (работает, но невидима на экране) вызывается
# функция 	focus
# для демонстрации сверните  запущенную программу.
def focus_demo(xx):
	if(xx):
		appuifw.note(ru('Aun_appuifw.py стала активной (foreground)'),'info')
	else:
		appuifw.note(ru('Aun_appuifw.py першла в фоновый режим (background)'),'info',1)
		
appuifw.app.focus = focus_demo 	# функция focus_demo объявляется
								# синонимом системной: appuifw.app.focus
	
def note_conf():
# appuifw.note(text[,'conf'[,global]])
# вывод окна сообщений (время около 3 секунд) 
# при global=1  сообщение выводится из фоного режима для программы, когда
# она свернута (не видима на экране)
	appuifw.note(ru('в type значение conf'),'conf')	
	
def note_error():
# appuifw.note(text[,'error'[,global]])
# вывод окна сообщений (время около 3 секунд) 
# при global=1  сообщение выводится из фоного режима для программы, когда
# она свернута (не видима на экране)
	appuifw.note(ru('в type значение error'),'error') 	
	
def selection_list():	
# appuifw.selection_list(choices[search_field=0])
# выбор в очень длинном списке (список занимает более одного окна) одной строки
# по шаблону вводимому с клавиатуры при search_field=1
# при   search_field=0 ввод с клавиатуры шаблона игнорируется, выбор только прокруткой
	index = appuifw.selection_list(List_Demo() , search_field=1)
	print u'selection_list'
	print u'List[',index,']=',List_Demo()[index]	
	
def multi_selection_list(x):
 # appuifw.multi_selection_list(choices[,style='checkbox',search_field=0])
 # выбор в списке строк (выбрать можyо несколько) при помощи установки флажков
 #  флажки ставятся нажатием на джойстик (центральную клавишу выбора)
 # выбор подтверждается нажатием на левую клавишу выбора ('OK')
 # есть отбор по  шаблону вводимому с клавиатуры 
 # при ,style='checkbox' флажки слева, при style='checkmark' флажки справа
 # при  style='checkmark' флажки устанавливаются при одновременном нажатии
 # клавиши 'Shift' и джойстика (центральная клавиша выбора)
 # !!!!! ИНТЕРЕСНО КАК ПОЛЬЗОВАТЕЛЬ ОБ ЭТОМ ДОГАДАЕТСЯ ????
	if x == 0 :
		index = appuifw.multi_selection_list(List_Demo() , style='checkbox', search_field=1)
		print u'multi_selection_list checkbox'
		print u'index=',index
	else :	
		index = appuifw.multi_selection_list(List_Demo() , style='checkmark',search_field=1)
		print u'multi_selection_list checkmark'
		print u'index=',index	
	
def query_text():
# appuifw.query(label,'text'[,initial_valye])
# ввод строки
# в initial_valye можно ввести строку по умолчанию 
# если пользователь нажал клавишу 'отмена', то возращается значение = None 
	print u'text=', appuifw.query (ru('Ввод текстовой строки'),'text')

def query_code():
# appuifw.query(label,'code'[,initial_valye])
# ввод строки для паролей 
# в initial_valye можно ввести строку по умолчанию 
# если пользователь нажал клавишу 'отмена', то возращается значение = None 	
	print u'code=', appuifw.query (ru('Ввод для паролей'),'code')
	
def query_number():
# appuifw.query(label,'number'[,initial_valye])
# ввод целого числа с защитой от некорректного ввода
# в initial_valye можно ввести число по умолчанию 
# если пользователь нажал клавишу 'отмена', то возращается значение = None 	
	print u'number=',appuifw.query (ru('Ввод целого'),'number')
	
def query_date():
# appuifw.query(label,'date'[,initial_valye])
# ввод даты с защитой от некорректного ввода
# в initial_valye можно ввести дату по умолчанию 
# если пользователь нажал клавишу 'отмена', то возращается значение = None
	t_date_UTC = appuifw.query (ru('Ввод даты'),'date',time.time())
	# time.time() возвращает текущее время (тип float) в секундах от  00:00:00 1 января 1970
	# дата, в формате времени,  возвращается как UTC
	print u'date=',time.strftime('%d.%m.%Y',time.localtime(t_date_UTC)) 
	# time.localtime - преобразует тип float в 'time tuple' вида:
	# (tm_year, tm_mon,tm_day, tm_hour, tm_min, tm_sec,tm_wday, tm_yday, tm_isdst)
	# c учетом локального времени
	
def query_time():
# appuifw.query(label,'time'[,initial_valye])
# ввод времени с защитой от некорректного ввода
# в initial_valye можно ввести время по умолчанию 
# если пользователь нажал клавишу 'отмена', то возращается значение = None
	if time.daylight == 0 :
		t_local = time.time() - time.timezone 
		# если телефоном непредусмотрен  переход на летнее время 
	else :
		t_local = time.time() - time.altzone
		# если телефоном предусмотрен переход на летнее время
	# в t_local текущее время (тип float) в секундах от  00:00:00 1 января 1970
	# с учетом текущей зоны и перехода на летнее время
	t_UTC = appuifw.query (ru('Ввод времени'),'time',t_local)
	print u'time=',time.strftime('%H:%M',time.gmtime(t_UTC))
	# time.gmtime - преобразует тип float в 'time tuple' вида:
	# (tm_year, tm_mon,tm_day, tm_hour, tm_min, tm_sec,tm_wday, tm_yday, tm_isdst)
	# без учета текущей зоны

def query_query():
# appuifw.query(label,'query')
# ввод выбора Да/Отмена
# если пользователь нажал клавишу 'отмена', то возращается значение = None	
	print u'query=', appuifw.query (ru('Вопрос ВЫ Согласны ДА / ОТМЕНА'),'query')
	
def query_float():	
# appuifw.query(label,'number'])
# ввод действительного числа с защитой от некорректного ввода
# при русской клавиатуре на телефоне разделитель 'запятая' 
# если пользователь нажал клавишу 'отмена', то возращается значение = None 
	print u'float=', appuifw.query (ru('Ввод действительных'),'float')

def main_menu_setup():
# главное меню на левой кнопке
	global old_body
	main_menu()
	appuifw.app.body = old_body
	appuifw.app.title = u'appuifw'

def main_menu():
	appuifw.app.menu = [(u'multi_query', multi_query),
						(u'note',
							((u'info', note_info),
							(u'conf', note_conf),
							(u'error', note_error))),
						(u'selection_list', selection_list),
						(u'multi_selection_list',
							((u'checkbox', lambda : multi_selection_list(0)),
							(u'checkmark', lambda : multi_selection_list(1)))),
						(u'query',
							((u'text', query_text),
							(u'code', query_code),
							(u'number', query_number),
							(u'date', query_date),
							(u'time', query_time),
							(u'query', query_query),
							(u'float', query_float))),	
						(u'Form Type', 
							((u'Flags=0', lambda : Form_Type()),
							(u'FFormEditModeOnly', lambda : Form_Type(appuifw.FFormEditModeOnly)),
							(u'FFormViewModeOnly', lambda : Form_Type(appuifw.FFormViewModeOnly)),
							(u'FFormAutoLabelEdit', lambda : Form_Type(appuifw.FFormAutoLabelEdit)),
							(u'FFormAutoFormEdit', lambda : Form_Type(appuifw.FFormAutoFormEdit)),
							(u'FFormDoubleSpaced', lambda : Form_Type(appuifw.FFormDoubleSpaced)))),
						(u'Text Type', text_type_menu_setup),
						(u'Listbox Type',Listbox_Type),
						(u'Canvas Type',Canvas_Type),
						(u'Tabs', navigation_tabs_set)]

						
# ====   Секция Form    ================== #	

# class Form(fields[, flags=0 ])
# где fields это список из полей вида (label, type[, value ])
# 	где label - строка в юникоде
#	где type - одна из строк (jописывает тип поля): 'text', 'number', 'date', 'time', 'combo', 'float'
#	где value - начальное значение (значение по умолчанию)
# где flags - это константы. определяющие способ работы с формой:
# FFormEditModeOnly, FFormViewModeOnly, FFormAutoLabelEdit, FFormAutoFormEdit, FFormDoubleSpaced
# 
# класс предназначен для ввода разнотипной информации с одного экрана
# в зависимости от значения flags на левой софт клавише меняется меню
# в данной программе конец редактирования формы - правая софт клавиша (назад)
def Form_Type(flags=0):
	global My_Form
	Form_execute(flags) # запуск на заполнение формы
	# печать My_Form после выхода из нее:
	print u'**********'
	# определим сколько записей в My_Form 
	# т.к. флаг FFormAutoFormEdit может изменять количество записей
	index_max = len(My_Form)
	# Доступ к первой записи My_Form осуществляется так:
	#  My_Form[0][0]='Фамилия', My_Form[0][1]='text', My_Form[0][2] ='Иванов'
	# Доступ ко второй записи My_Form осуществляется так:
	#  My_Form[1][0]='Фамилия', My_Form[1][1]='number', My_Form[1][2] =46
	# вывод всех полей формы:
	for index in range(0, index_max, 1):
		if My_Form[index][1] == 'combo' :
			index_list = My_Form[index][2][1] #  текущий индекс в списке My_town
			print My_Form[index][0],u'=',My_Form[index][2][0][index_list]
		else :	
			print My_Form[index][0],u'=',My_Form[index][2]
	
def Form_execute(flags):
	# заполнение формы
	global My_Form
	# текущее время для примера отображения 'time';
	if time.daylight == 0 :
		t_local = time.time() - time.timezone 
		# если телефоном непредусмотрен  переход на летнее время 
	else :
		t_local = time.time() - time.altzone
		# если телефоном предусмотрен переход на летнее время
	# список для демонстрации 'combo':
	My_town = [ru('Москва'),ru('Сургут'),ru('Саратов'),ru('Волгоград')]	
	# описание формы:
	My_List = [(ru('Фамилия'),'text',ru('Иванов')),
				(ru('Возраст'),'number',46),
				(ru('Год'),'date',time.mktime((1961, 01, 02, 0, 0,0, 0, 0, -1))),
				(ru('Время'),'time',t_local),
				(ru('Город'),'combo',(My_town,2)),
				(ru('Число  π'),'float',3.14)]
	My_Form = appuifw.Form(My_List,flags)
	My_Form.menu = [(u'My_callback 0', lambda :My_callback(0)),
					(u'My_callback 1', lambda :My_callback(1))]				
	My_Form.execute() # запуск формы на отображение/заполнение
	
def My_callback(x):
	# написано для демонстации вызова из меню My_Form	
	if x :
		appuifw.note(ru('My_callback = 1'),'info')
	else :
		appuifw.note(ru('My_callback = 0'),'info')

		
# ====   Секция Text    ================== #	

def Str_demo():return ru('Съешь ещё этих мягких французских булок, да выпей чаю. 1234567890   ')
# формирование строки, для демонстрации работы с атрибутами текста

def text_font():
# выбор шрифта
	global My_Text
	fonts=appuifw.available_fonts()
	fonts.sort()
	font_index=appuifw.popup_menu(fonts,ru('Есть шрифты'))
	My_Text.font=fonts[font_index]
	My_Text.add(fonts[font_index])
	My_Text.add(Str_demo())

def T_STILE():
# выбор стиля шрифта
	global My_Text
	St = [u'STYLE_BOLD', u'STYLE_UNDERLINE', u'TYLE_ITALIC', u'STYLE_STRIKETHROUGH', 
			u'HIGHLIGHT_ROUNDED', u'HIGHLIGHT_SHADOW', u'HIGHLIGHT_STANDARD']
		
	index = appuifw.multi_selection_list(St , style='checkbox', search_field=1)
	My_Text.style = 0
	if 0 in index : My_Text.style = My_Text.style | appuifw.STYLE_BOLD
	if 1 in index : My_Text.style = My_Text.style | appuifw.STYLE_UNDERLINE
	if 2 in index : My_Text.style = My_Text.style | appuifw.STYLE_ITALIC
	if 3 in index : My_Text.style = My_Text.style | appuifw.STYLE_STRIKETHROUGH
	if (4 in index)&(5 in index) : My_Text.style = My_Text.style|appuifw.HIGHLIGHT_ROUNDED
	# HIGHLIGHT_ROUNDED и HIGHLIGHT_SHADOW не допускается использовать совместно
	else :
		if 4 in index : My_Text.style = My_Text.style | appuifw.HIGHLIGHT_ROUNDED
		if 5 in index : My_Text.style = My_Text.style | appuifw.HIGHLIGHT_SHADOW
	if 6 in index : My_Text.style = My_Text.style | appuifw.HIGHLIGHT_STANDARD	
	My_Text.add(Str_demo())	

def T_color():
# выбор цвета шрифта
	global My_Text
	St = [ru('красный'), ru('зелёный'), ru('голубой'), ru('розовый'), ru('оранжевый'),
			ru('синий'), ru('темн.зелёный'),ru('чёрный'),ru('белый')]
	St_color = ((255,0,0),(0,255,0),(0,0,255),(255,0,255),(255,128,0),
				(0,0,128),(0,128,0),(0,0,0),(255,255,255))		
	St_index = appuifw.popup_menu(St,ru('Цвет шрифта'))
	My_Text.color = St_color[St_index]
	My_Text.add(Str_demo())
		
def T_highlight_color():
# выбор цвета фона  шрифта  при выборе стилей:
# HIGHLIGHT_ROUNDED, HIGHLIGHT_SHADOW
	global My_Text
	St = [ru('бледно красный'), ru('бледно зелёный'), ru('бледно голубой'), ru('розовый'),
			ru('серый'),ru('белый')]
	St_color = ((255,128,128),(0,255,128),(128,255,255),(255,128,255),
				(192,192,192),(255,255,255))		
	St_index = appuifw.popup_menu(St,ru('Цвет шрифта'))
	My_Text.highlight_color = St_color[St_index]
	My_Text.add(Str_demo())
	
def text_type_menu():
#  меню text на левой кнопке в режиме text
	appuifw.app.menu = [(u'fonts', text_font),
						(u'STYLE', T_STILE),
						(ru('Цвет шрифта'), T_color),
						(ru('Цвет фона'), T_highlight_color),
						(u'Tabs', navigation_tabs_set),
						(ru('Выход из Text'), main_menu_setup)]

def text_type_menu_setup(x=0):
#  text_type_menu_setup может быть вызвана с одним параметром или без параметров. 
# Если она вызвана без параметров, то по умолчанию параметру x присваивается 
# значение 0.
#
# инициализация  Text
	global My_Text
	appuifw.app.body = My_Text
	appuifw.app.title = u'Text'
	text_type_menu()
	if x == 0 :
		appuifw.note(ru('цвета фона ТОЛЬКО в стилях: HIGHLIGHT_ROUNDED, HIGHLIGHT_SHADOW'),'info')
	if 	My_Text.len() == 0 :
		My_Text.add(Str_demo())
	
# ====   Секция Listbox    ================== #
	
def Listbox_Type(begin=28,end=38):
	# для демонстрации создается список с иконками из системного
	# файла avkon.mbm (avkon2.mbm для Symbian 9)
	global list_Listbox_Type
	list_Listbox_Type = []
	Vers = e32.s60_version_info
	# начиная с Symbian 9 расположение файлов ресурсов изменилось. проверяем версию
	if Vers[0] < 3 :
		list_Listbox_Type.append((ru('Диапазон иконок'),
								appuifw.Icon(u'z:\\system\\data\\avkon.mbm', begin, begin+1)))
		for index in range(begin+2, end, 2):
			list_Listbox_Type.append((u'icon %s, %s' % (index, index+1),
								appuifw.Icon(u'z:\\system\\data\\avkon.mbm', index, index+1)))
	else:
		list_Listbox_Type.append((ru('Диапазон иконок'),
								appuifw.Icon(u'z:\\resource\\apps\\avkon2.mbm', begin, begin+1)))
		for index in range(begin+2, end, 2):
			list_Listbox_Type.append((u'icon %s, %s' % (index, index+1),
									appuifw.Icon(u'z:\\resource\\apps\\avkon2.mbm', index, index+1)))
								
								
	appuifw.app.title = u'Listbox'							
	appuifw.app.body = appuifw.Listbox(list_Listbox_Type, Listbox_index)

def	Listbox_index():
	global list_Listbox_Type
	index = appuifw.app.body.current()
	# первый элемент Lixbox используется для выбора диапазона использования (просмотра) иконок
	# остальные элементы вызывают переход в окно Python и отладочную печать
	if index == 0:
		ico_begin = appuifw.query(ru('Иконка начиная с'),'number',28)
		ico_end = appuifw.query(ru('Иконка последний номер'),'number',252)
		Listbox_Type(ico_begin,ico_end)	
	else:
		print u'Index Listbox=',index
		appuifw.app.body = old_body
		appuifw.app.title = u'appuifw'
		
# ====   Секция Canvas   =================== #
		
def	Canvas_Type():
	# class Canvas([redraw callback=None, event callback=None, resize callback=None ])
	# redraw callback - имя функции обновляющией (перерисовывающей экран).
	#  необходима, т.к. при перекрытии области Canvas окнами элементов управления
	#  рисунки Canvas "бледнеют".
	# event callback - имя функции обрабатываюшей код ажатой клавиши
	# resize callback - имя функции обрабатываюшей  изменения размера,
	# 
	# Можно рисовать непосредственно на области Canvas, но только в том случае,
	# если ненужно обновлять экран. Удобнее рисовать на элементе graphics.Image
	# и выводить его содержимое в  Canvas через операцию redraw callback
	
	global	My_Canvas, My_img, My_outline, My_width, My_fill
	appuifw.app.title = u'Canvas'
	My_width = 1
	My_outline = (255,0,255)
	My_fill = (0,255,0)
	appuifw.app.body = My_Canvas = appuifw.Canvas(redraw_callback = redraw_My_Canvas, event_callback = Ccnvas_Key)
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	My_img = graphics.Image.new((x_max,y_max)) # область для рисования
	Canvas_line()
	redraw_My_Canvas((x_max,y_max))
	Canvas_menu()
	
My_img = None
My_img_pattern = None

def redraw_My_Canvas(x):
	# в x передается информация о координатах области перерисовки
	global	My_img, My_Canvas
	if My_img :
		My_Canvas.blit(My_img) # обновление (перерисовывание) экрана My_Canvas из картинки 
	
def	Canvas_line():
	# line(coordseq[, <options>])
	# coordseq - координаты определяют начало и конец линии
	global	My_img, My_width, My_outline
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	# рисование двух диагоналей:
	My_img.line((0,0,x_max,y_max), outline = My_outline, width = My_width)
	My_img.line((x_max,0,0,y_max), outline = My_outline, width = My_width)
	
def	Canvas_polygon():
	# polygon(coordseq[, <options>])
	# coordseq - координаты определяют вершины полигона
	global	My_img, My_width, My_outline, My_img_pattern
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	if My_img_pattern == None :
		My_img.polygon((x_max/2,y_max/2-y_max/4,x_max/2-x_max/4,y_max/2+y_max/4,x_max/2+x_max/4,y_max/2+y_max/4),
					outline = My_outline, fill = My_fill, width = My_width)
	else :
		My_img.polygon((x_max/2,y_max/2-y_max/4,x_max/2-x_max/4,y_max/2+y_max/4,x_max/2+x_max/4,y_max/2+y_max/4),
					outline = My_outline, fill = My_fill, width = My_width, pattern = My_img_pattern)
	
def Canvas_rect():
	# rectangle(coordseq[, <options>])
	# coordseq - координаты определяют верхний левый и нижний правый угол
	#  прямоугольника
	global	My_img, My_width, My_outline, My_fill, My_img_pattern
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	if My_img_pattern == None :
		My_img.rectangle((x_max/2-x_max/8,y_max/2-y_max/4,x_max/2+x_max/8,y_max/2+y_max/4),
							outline = My_outline, fill = My_fill, width=My_width)
	else :
		My_img.rectangle((x_max/2-x_max/8,y_max/2-y_max/4,x_max/2+x_max/8,y_max/2+y_max/4),
							outline = My_outline, fill = My_fill, width=My_width, pattern = My_img_pattern)
	
def Canvas_point():
	# point(coordseq[, <options>])
	# coordseq - координаты определяют положение точки 
	global	My_img, My_width, My_outline
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	My_img.point((x_max/2-20,y_max/2), outline = My_outline, width=My_width)
	
def Canvas_ellipse():
	# ellipse(coordseq[, <options>])
	# coordseq - координаты определяют верхний левый и нижний правый угол
	# вписанного в эллипс прямоугольника
	global	My_img, My_width, My_outline, My_fill, My_img_pattern
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	if My_img_pattern == None :
		My_img.ellipse((x_max/2-x_max/4,y_max/2-y_max/4,x_max/2+x_max/4,y_max/2+y_max/4), 
						outline = My_outline, fill = My_fill, width=My_width)
	else :
		My_img.ellipse((x_max/2-x_max/4,y_max/2-y_max/4,x_max/2+x_max/4,y_max/2+y_max/4), 
						outline = My_outline, fill = My_fill, width=My_width, pattern = My_img_pattern)

def Canvas_pieslice():
	# pieslice(coordseq, start, end[, <options>])
	# 	выводится сектор, вырезанный из эллипса
	# coordseq - координаты определяют верхний левый и нижний правый угол
	# 	вписанного в эллипс прямоугольника
	# start - начальный угол для сектора отсчитывается от правой полуоси эллипса
	# end - конечный угол  для сектора отсчитывается от правой полуоси эллипса
	# углы в радианах,
	global	My_img, My_width, My_outline, My_fill, My_img_pattern
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	if My_img_pattern == None :
		My_img.pieslice((x_max/2-x_max/4,y_max/2-y_max/4,x_max/2+x_max/4,y_max/2+y_max/4),0, 3.14/3,
						outline = My_outline, fill = My_fill, width=My_width)
	else :
		My_img.pieslice((x_max/2-x_max/4,y_max/2-y_max/4,x_max/2+x_max/4,y_max/2+y_max/4),0, 3.14/3,
						outline = My_outline, fill = My_fill, width=My_width, pattern = My_img_pattern)
	
					
def Canvas_arc():
	# arc(coordseq, start, end[, <options>])
	# 	выводится дуга, вырезанная из эллипса
	# coordseq - координаты определяют верхний левый и нижний правый угол
	# 	вписанного в эллипс прямоугольника
	# start - начальный угол для дуги отсчитывается от правой полуоси эллипса
	# end - конечный угол  для дуги отсчитывается от правой полуоси эллипса
	# углы в радианах,
	global	My_img, My_width, My_outline, My_fill
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	My_img.arc((x_max/2-x_max/4,y_max/2-y_max/4,x_max/2+x_max/4,y_max/2+y_max/4),
					0, 3.14/3, outline = My_outline, width = My_width)
					
def Canvas_txt():
	# text(coordseq, text[fill=0, font=u”LatinBold12” ])
	# coordseq - координаты определяют положение начала строки
	global	My_img, My_outline
	My_img.clear() # сброс к цвету по умолчанию
	# вывод  шрифтов с логическими именами (странно, но имена должны быть не в юникоде):
	My_img.text((0,15), ru('Шрифт этот normal'), fill = My_outline, font = 'normal')
	My_img.text((0,30), ru('Шрифт этот dense'), fill = My_outline, font = 'dense')				
	My_img.text((0,45), ru('Шрифт этот symbol'), fill = My_outline, font = 'symbol')
	My_img.text((0,60), ru('Шрифт этот legend'), fill = My_outline, font = 'legend')		
	My_img.text((0,75), ru('Шрифт этот annotation'), fill = My_outline, font = 'annotation')
	My_img.text((0,90), ru('Шрифт этот title'), fill = My_outline, font = 'title')
	# вывод шрифтов, которые есть в системе.
	fonts=appuifw.available_fonts()
	index_max = len(fonts)
	for index in range(0, index_max, 1):
		My_img.text((0,105+index*15), ru('Шрифт этот ')+fonts[index], font = fonts[index])
						
def set_outline():
	global	My_outline
	St = [ru('красный'), ru('зелёный'), ru('голубой'), ru('розовый'), ru('оранжевый'),
			ru('синий'), ru('темн.зелёный'),ru('чёрный'),ru('белый')]
	St_color = ((255,0,0),(0,255,0),(0,0,255),(255,0,255),(255,128,0),
				(0,0,128),(0,128,0),(0,0,0),(255,255,255))		
	St_index = appuifw.popup_menu(St,ru('Цвет контура'))
	My_outline = St_color[St_index]

def set_fill():
	global	My_fill
	St = [ru('красный'), ru('зелёный'), ru('голубой'), ru('розовый'), ru('оранжевый'),
			ru('синий'), ru('темн.зелёный'),ru('чёрный'),ru('белый')]
	St_color = ((255,0,0),(0,255,0),(0,0,255),(255,0,255),(255,128,0),
				(0,0,128),(0,128,0),(0,0,0),(255,255,255))		
	St_index = appuifw.popup_menu(St,ru('Цвет заливки'))
	My_fill = St_color[St_index]
	
def set_width():
	global	My_width
	x = My_width
	My_width = appuifw.query (ru('width (толщина)'),'number', x)

def Canvas_clear():
	# clear([color=0xffffff ])
	# color - сбросить к заданному цвету
 	global	My_img
	My_img.clear() # сброс к цвету по умолчанию
	
def Convas_pattern(x):	
	# рисование объекта My_img_pattern, который может использоваться как образец
	# для заполнения фона в фигурах.
	# параметр x определяет надо ли создавать образец
	# образец может быть любым черно - белым рисунком. 
	global	My_img_pattern, My_width, My_fill
	if x == 1:
		x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
		My_img_pattern = graphics.Image.new((x_max,y_max), mode = '1') # область для рисования черно белого образца
		# в качестве образца создается штриховка под 45 градусов с шагом 7 пикселей:
		index_end = 2*y_max/7
		for k in range(index_end):
			My_img_pattern.line((0, y_max - 7*k ,7*k, y_max), outline = 0, width = My_width)
	else:
			My_img_pattern = None
		
def Ccnvas_Key(x):
	# функция выводит 4 строки текста
	# при нажатии на кнопку клавиатуры
	# информация о кнопке перелается через x:
	# (x['scancode'], x['modifiers'], x['type'], x['keycode'])
	# мнемоники для кодов можно взять из key_codes.py 
	
	global	My_img
	x_max,y_max = My_Canvas.size # атрибут возвращает размеры области рисования
	# стераем область вывода текста с предыдущими данными
	My_img.rectangle((x_max/2-50,y_max-65,x_max/2+50,y_max), fill = (255,255,255))
	
	My_img.text((x_max/2-50,y_max-50), u' scancode =' + hex(x['scancode']))
	My_img.text((x_max/2-50,y_max-35), u'modifiers =' + hex(x['modifiers']))
	My_img.text((x_max/2-50,y_max-20), u'     type =' + hex(x['type']))
	My_img.text((x_max/2-50,y_max-5), u'  keycode =' + hex(x['keycode']))
	# принудительно перерисовываем Canvas, для отображения выведенного текста:
	redraw_My_Canvas(())
	
def Canvas_menu():
	global	My_Canvas, My_img_pattern
	appuifw.app.menu = [(u'line', Canvas_line),
						(u'polygon', Canvas_polygon),			
						(u'rectangle', Canvas_rect),
						(u'point', Canvas_point),
						(u'ellipse',Canvas_ellipse),
						(u'pieslice',Canvas_pieslice),
						(u'arc',Canvas_arc),
						(u'Text', Canvas_txt),
						(u'options', 
							((u'outline', set_outline),
							(u'fill',set_fill ),
							(u'width', set_width), 
							(u'pattern ON', lambda :Convas_pattern(1) ),
							(u'pattern OFF', lambda :Convas_pattern(0) ))),
						(u'clear', Canvas_clear),
						(ru('Выход из Canvas'), main_menu_setup)]

# ====   Секция Tabs   ===================== #
def tabs_menu():
#  меню text на левой кнопке в режиме Tabs
	appuifw.app.menu = [(ru('Отключить Tabs'), navigation_tabs_OFF)]
								
def navigation_tabs_set():
	global list_Listbox_Type,My_Text
	# создаем элемент tabs из 4 вкладок с функцией обработки navigation_tabs:
	appuifw.app.set_tabs([u'Old', u'Text', u'Listbox', u'Canvas'],navigation_tabs)
	tabs_menu()
	# устанавливаем  индекс Tab в положение, соответствующее
	# текущему окну (appuifw.app.body)
	# appuifw.app.body - использовано, что бы не вводить еще одну global
	if appuifw.app.title == u'appuifw':
		index=0
	elif appuifw.app.title == u'Text':
		index=1
	elif appuifw.app.title == u'Listbox':
		index=2
	elif appuifw.app.title == u'Canvas':
		index=3
	appuifw.app.activate_tab(index)
	navigation_tabs(index)

def navigation_tabs(index):
	# функция, которая вызывается при перемещении с текущей вкладки tabs
	global My_Text	
	if (index == 0):
		appuifw.app.body = old_body
		appuifw.app.title = u'appuifw'
	elif (index == 1):
		text_type_menu_setup(1)
	elif (index == 2):
		Listbox_Type()
	elif (index == 3):
		Canvas_Type()	
	print 'Index Tab=',index
	tabs_menu()	
	
def navigation_tabs_OFF():
	appuifw.app.set_tabs([],lambda x: None)		
	if appuifw.app.title == u'Text':
		text_type_menu()
	elif appuifw.app.title == u'Canvas':
		Canvas_menu()
	else :
		main_menu()

def exit_key_handler():
    app_lock.signal()
		
#--------Собственно программа--------------------- #
old_body=appuifw.app.body # запоминание окружения из которого производился запуск
appuifw.app.screen='normal' 
main_menu_setup() # активизация основного меню
appuifw.note(ru('нажмите левую софт клавишу'),'info')
#
# Перевод программы в режим ожидания событий (например нажатие клавиши, сигнал таймера,
#   сигнал от другой программы). Для обработки событий должны быть написаны соответствующие
#   функции (def).
# В данной прграмме, после ее запуска и перехода в режим ожидания нажатие на левую софт клавишу 
#   приводит к запуску функции выбора меню, в данном случае функции: main_menu()
app_lock = e32.Ao_lock()
appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()			