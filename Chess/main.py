#*- coding: utf-8 -*-
from model import *
from view import *

class ChessGame(object):
	"""
	主类
	"""
	def __init__(self):
		"""
		应用初始化
		"""
		#棋盘初始化......后端
		self.board = ChessBoard()
		#界面初始化......前端
		self.view = ChessView(self)
		#是否以点击过
		self.clicked = False
		self.i0, self.j0 = 0, 0
		

	def button_1_callback(self, event):
		print event.x, event.y
		
		i = self.view.get_idx(event.x)
		j = self.view.get_idx(event.y)
		
		if self.clicked is False:
			piece = self.board.loc[i, j]
			if piece: 
				piece.state = 'S'
				self.view.draw(self.board)
				self.i0, self.j0 = i, j
				self.clicked = True
		else:
			piece = self.board.loc[self.i0, self.j0]
			piece.state = ''
			di, dj = i - self.i0, j - self.j0
			if piece.move_check(i, j, di, dj) and self.board.move_check(i, j, piece.color):
				self.board.loc[i, j] = piece
				self.board.loc[self.i0, self.j0] = None
			self.view.draw(self.board)
			self.clicked = False

	def start(self):
		"""
		开始
		"""
		#界面绘制
		self.view.draw(self.board)
		#进入主循环
		self.view.mainloop()

game = ChessGame()
game.start()
