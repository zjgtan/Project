#!/usr/bin/env python
#-*- coding: utf-8 -*-
import Tkinter
import Image, ImageTk

root = Tkinter.Tk()
root.title("Chinese Chess")

can = Tkinter.Canvas(root, width=373, height=410)
can.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)

"""
棋盘图片
"""
img = Tkinter.PhotoImage(file="./images/WHITE.gif")
can.create_image(0, 0, image=img, anchor=Tkinter.NW)

def get_coord(x):
	return 30 + 40 * x

img_RK = Tkinter.PhotoImage(file="./images/RK.gif")
image_RK = can.create_image(get_coord(4), get_coord(0), image=img_RK)
can.create_image(get_coord(4), get_coord(2), image=img_RK)
can.create_image(get_coord(3), get_coord(6), image=img_RK)

def get_idx(x):
	if x <= 50:
		return 0
	else:
		return (x-50)/40 + 1

import copy

def do_mouse(event):
	if get_idx(event.x) == 4 and get_idx(event.y) == 0:
		print "get_mouse"

		#can = Tkinter.Canvas(root, width=373, height=410)
		#can.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)

		"""
		棋盘图片
		"""
		#img = Tkinter.PhotoImage(file="./images/WHITE.gif")
		#can.create_image(0, 0, image=img, anchor=Tkinter.NW)
	
		global img_RKS
		img_RKS = Tkinter.PhotoImage(file="./images/RKS.gif")
		can.delete(image_RK)
		can.create_image(get_coord(4), get_coord(1), image=img_RKS)

can.bind('<Button-1>', do_mouse)

root.mainloop()
