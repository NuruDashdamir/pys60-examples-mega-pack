# Magic Video 1.0
# Copyright (C) 2007-2009 Floriano Scioscia
#
# A video numbers puzzle for Python S60
#
# This program is free software; you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation;
# either version 2 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

import random
import math
import time
import e32
import appuifw
import camera
import graphics
from appuifw import Form
from graphics import Image
from key_codes import * 

SIS_VERSION=u"1.0.0"

class MagicVideo:
	
	def __init__(self):
		s = appuifw.app.layout(appuifw.EMainPane)[0] # drawing area size
		self.x = s[0]
		self.y = s[1]
		self.frame = Image.new((self.x, self.y))   # for double buffering
		#DEBUG self.frames = 0
		self.victory = u'Congratulations!'
		self.entropy_num = 3
		self.entropy_den = 4
		self.SELECTED_TILE_COLOR = (255,0,0)
		self.EMPTY_TILE_COLOR = (255,255,128)
		self.new_game(16)
	
	def new_game(self, n):
		self.n = n                        # pieces
		self.r = int(math.sqrt(self.n))   # rows/cols
		self.w = self.x / self.r          # piece width
		self.h = self.y / self.r          # piece height
		self.seq = range(self.n)
		self.shuffle()
		self.selected = 0
		self.state = u'play'
		self.frame.clear()
	
	def shuffle(self):
		blank = self.seq.index(self.n-1)
		k = 0
		while k < self.n * 2 or self.entropy() < self.n*self.entropy_num/self.entropy_den:
			(br, bc) = self.n2rc(blank)
			k += 1
			d = random.randint(1,4)
			if d == 1 and br > 0: # up
				self.swap(blank, blank - self.r)
				blank -= self.r
			elif d == 2 and br < self.r-1: # down
				self.swap(blank, blank + self.r)
				blank += self.r
			elif d == 3 and bc > 0: # left
				self.swap(blank, blank - 1)
				blank -= 1
			elif d == 4 and bc < self.r-1: # right
				self.swap(blank, blank + 1)
				blank += 1
	
	def entropy(self):
		d = 0
		for i in range(self.n):
			if self.seq[i] != i:
				d += 1
		return d
	
	def run(self):
		# setup screen
		appuifw.app.screen = 'large'
		appuifw.app.title = u'Magic Video'
		appuifw.app.exit_key_handler = self.stop
		appuifw.app.body = appuifw.Canvas(event_callback = self.event)
		appuifw.app.menu = [(u"Effortless (2x2)", lambda: self.new_game(4)), (u"Easy (3x3)", lambda: self.new_game(9)), (u"Medium (4x4)", lambda: self.new_game(16)), (u"Hard (5x5)", lambda: self.new_game(25)), (u"Impossible (6x6)", lambda: self.new_game(36)), (u"Help", self.help), (u"About Magic Video", self.about)]
		self.prerender_text()
		camera.start_finder(self.draw) 		# start camera
		self.lock = e32.Ao_lock()
		self.lock.wait()
		camera.stop_finder()
		camera.release()
	
	def stop(self):		
		self.lock.signal()
	
	def about(self):
		appuifw.note(u'Magic Video ' + SIS_VERSION + u'\n(C) 2007-2009 Floriano Scioscia\nfloriano.scioscia@libero.it\nEnjoy!')
		
	def help(self):
		appuifw.note(u'1/3\nThe goal is to recompose the picture, very much like the famous "Fifteen puzzle" game.')
		appuifw.note(u'2/3\nUse direction keys to move the red box that marks the selected tile.')
		appuifw.note(u'3/3\nPress the center key to swap the selected tile with the empty tile.\nHave fun!')

	def prerender_text(self):
		tr = appuifw.app.body.measure_text(self.victory, font='title')[0]
		self.text_pos = ((self.x - tr[2] + tr[0]) / 2, (self.y - tr[3] + tr[1]) / 2, (self.x + tr[2] - tr[0]) / 2, (self.y + tr[3] - tr[1]) / 2)
		self.text_img = Image.new((tr[2]-tr[0] + 2, tr[3]-tr[1] + 2))
		self.text_img.clear()
		self.text_img.text((-tr[0]+2, -tr[1]+2), self.victory, fill=(64,64,64), font='title')
		self.text_img.text((-tr[0], -tr[1]), self.victory, fill=(0,0,255), font='title')
		self.text_mask = Image.new((tr[2]-tr[0] + 2, tr[3]-tr[1] + 2), mode='L')
		self.text_mask.clear(0)
		self.text_mask.text((-tr[0]+2, -tr[1]+2), self.victory, fill=(255,255,255), font='title')
		self.text_mask.text((-tr[0], -tr[1]), self.victory, fill=(255,255,255), font='title')
	
	def draw(self, im):
		s = im.size
		step_x = s[0] / self.r
		step_y = s[1] / self.r
		for i in range(self.n):
			src_x = step_x * (self.seq[i] % self.r)
			src_y = step_y * int(math.floor(self.seq[i] / self.r))
			des_x = self.w * (i % self.r)
			des_y = self.h * int(math.floor(i / self.r))
			if self.seq[i] == self.n-1:
				self.frame.rectangle((des_x, des_y, des_x + self.w + 1, des_y + self.h + 1), fill=self.EMPTY_TILE_COLOR)
			else:
				self.frame.blit( im, target=(des_x, des_y, des_x + self.w + 1, des_y + self.h + 1), source=(src_x, src_y, src_x + step_x, src_y + step_y), scale=1)
			if i == self.selected:
				self.frame.rectangle((des_x, des_y, des_x + self.w - 1, des_y + self.h - 1), width=3, outline=self.SELECTED_TILE_COLOR, fill=None)
		if self.state == u'win':
			self.frame.blit(self.text_img, target=self.text_pos, mask=self.text_mask)
		appuifw.app.body.blit(self.frame)
		#DEBUG self.frames += 1
	
	def n2rc(self, n):
		r = int(math.floor(n / self.r))
		c = n % self.r
		return (r, c)
	
	def swap(self, p1, p2):
		temp = self.seq[p1]
		self.seq[p1] = self.seq[p2]
		self.seq[p2] = temp
	
	def event(self, ev):
		if self.state == u'play':
			if ev['type'] == appuifw.EEventKey:
				(r1, c1) = self.n2rc(self.selected)
				k = ev['keycode']
				if k == EKeyUpArrow:
					if r1 > 0:
						self.selected -= self.r
				elif k == EKeyDownArrow:
					if r1 < self.r-1:
						self.selected += self.r
				elif k == EKeyLeftArrow:
					if c1 > 0:
						self.selected -= 1
				elif k == EKeyRightArrow:
					if c1 < self.r-1:
						self.selected += 1
				elif k == EKeySelect:
					blank = self.seq.index(self.n-1)
					(r2, c2) = self.n2rc(blank)  # position of blank piece
					if (r1==r2 and abs(c1-c2)==1) or (c1==c2 and abs(r1-r2)==1):
						self.swap(self.selected, blank)
						if self.seq == range(self.n):
							self.state = u'win'


# Startup
old_screen = appuifw.app.screen
old_body = appuifw.app.body
old_title = appuifw.app.title
old_menu = appuifw.app.menu
old_exit_handler = appuifw.app.exit_key_handler

v = MagicVideo()
#DEBUG t0 = time.clock()
v.run()
#DEBUG t1 = time.clock()
#DEBUG dt = t1 - t0

# Cleanup
appuifw.app.body = old_body
appuifw.app.title = old_title
appuifw.app.menu = old_menu
appuifw.app.exit_key_handler = old_exit_handler
appuifw.app.screen = old_screen
appuifw.app.set_exit()
#DEBUG print "%d frames, %f seconds, %f FPS, %f ms/frame."%(v.frames, dt, v.frames/dt, dt/v.frames*1000.)
