import camera,e32,socket,appuifw

def bluch():
	def start():
		image = camera.take_photo()
		
		appuifw.app.body = c =appuifw.Canvas()
		c.blit(image,scale=1)
		file=(u"e:\\Images\\aa.jpg")
		image.save(file)
		device=socket.bt_obex_discover()
		
		address=device[0]
		channel=device[1][u'OBEX Object Push']
		socket.bt_obex_send_file(address,channel,file)
		
		appuifw.note(u"picture sent","info")
		
	def quit():
		app_lock.signal()
		appuifw.app.set_exit()

	app_lock = e32.Ao_lock()
	appuifw.app.title  = u"Bluetooth_photo"
	appuifw.app.menu = [(u"Start",start),(u"Exit",quit)]
	
	app_lock.wait()

