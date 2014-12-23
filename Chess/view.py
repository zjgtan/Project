#-*- coding: utf-8 -*-
import Tkinter

image_mapping = {
		"Jiang" : 'K',
		"Shi" : 'A',
		"Xiang" : 'B',
		"Ju" : 'R',
		"Ma" : 'N',
		"Pao" : 'C',
		"Bing" : 'P'
		}

class ChessView(object):
	"""
	界面
	"""
	def __init__(self, control):	
		self.root = Tkinter.Tk()
		self.root.title("Chinese Chess")

		#画布层
		self.canvas = Tkinter.Canvas(self.root, width=373, height=410)
		self.canvas.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)
		
		#棋盘
		self.board_image = Tkinter.PhotoImage(file="./images/WHITE.gif") #必须有全局变量保留图片的引用
		self.canvas.create_image(0, 0, image=self.board_image, anchor=Tkinter.NW)
		
		#棋子
		self.loc_image = {} 
		#此处不直接初始化是考虑添加用户之前只有棋盘而没有棋子

		#注册外部中断
		self.control = control
		self.canvas.bind("<Button-1>", self.control.button_1_callback)

	def draw(self, board):
		
		for i in range(board.M):
			for j in range(board.N):
				piece = board.loc[i, j]
				if piece is None:
					try:
						self.canvas.delete(self.loc_image[i, j])
						self.loc_image[i, j] = None
					except:
						continue
				else:
					name = image_mapping[piece.__class__.__name__] #名称
					color = piece.color #颜色
					state = piece.state #状态
					self.loc_image[i, j] = Tkinter.PhotoImage(file="./images/"+color+name+state+".gif")
					self.canvas.create_image(self.get_coord(i), self.get_coord(j), image=self.loc_image[i, j])

	def get_coord(self, x):
		return 30 + 40 * x

	def get_idx(self, x):
		if x <= 50:
			return 0
		else:
			return (x - 50) / 40 + 1



	def mainloop(self):
		self.root.mainloop()

