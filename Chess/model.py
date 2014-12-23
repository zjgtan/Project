#-*- coding: utf-8 -*-

class ChessPiece(object):
	"""
	棋子基类
	"""
	def __init__(self):
		pass

	def move_check(self, dx, dy, board):
		pass
	

class Jiang(ChessPiece):
	"""
	将
	"""
	def __init__(self, color):
		self.color = color
		self.state = ''
	
	def move_check(self, x, y, dx, dy):
		if ((dx == 1 or dx == -1) and dy == 0) or (dx == 0 and (dy == -1 or dy == 1)):
			if self.color == "R" and  7 <= y <= 9 and 3 <= x <= 5:
				return True
			if self.color == "B" and 3 <= x <= 5 and 0 <= y <= 2:
				return True
				
		return False

class Shi(ChessPiece):
	"""
	士
	"""
	def __init__(self, color):
		self.color = color
		self.state = ''

	def move_check(self, dx, dy):
		return True

class Xiang(ChessPiece):
	"""
	象
	"""
	def __init__(self, color):
		self.color = color
		self.state = ''

	def move_check(self, dx, dy):
		return True

class Ju(ChessPiece):
	"""
	车
	"""
	def __init__(self, color):
		self.color = color
		self.state = ''

	def move_check(self, dx, dy):
		return True

class Ma(ChessPiece):
	"""
	马
	"""
	def __init__(self, color):
		self.color = color
		self.state = ''

	def move_check(self, dx, dy):
		return True

class Pao(ChessPiece):
	"""
	炮
	"""
	def __init__(self, color):
		self.color = color
		self.state = ''

	def move_check(self, dx, dy):
		return True

class Bing(ChessPiece):
	"""
	兵
	"""
	def __init__(self, color):
		self.color = color
		self.state = ''

	def move_check(self, dx, dy):
		return True

class ChessBoard(object):
	"""
	棋盘类
	"""

	def __init__(self):
		#棋盘上的位置
		self.loc = {}
		self.M, self.N = 9, 10

		for i in range(self.M):
			for j in range(self.N):
				self.loc[i, j] = None

		self.loc[0, 0] = Ju("B")
		self.loc[1, 0] = Ma("B")
		self.loc[2, 0] = Xiang("B")
		self.loc[3, 0] = Shi("B")
		self.loc[4, 0] = Jiang("B")
		self.loc[5, 0] = Shi("B")
		self.loc[6, 0] = Xiang("B")
		self.loc[7, 0] = Ma("B")
		self.loc[8, 0] = Ju("B")

		self.loc[1, 2] = Pao("B")
		self.loc[7, 2] = Pao("B")

		self.loc[0, 3] = Bing("B")
		self.loc[2, 3] = Bing("B")
		self.loc[4, 3] = Bing("B")
		self.loc[6, 3] = Bing("B")
		self.loc[8, 3] = Bing("B")
		
		self.loc[0, 9] = Ju("R")
		self.loc[1, 9] = Ma("R")
		self.loc[2, 9] = Xiang("R")
		self.loc[3, 9] = Shi("R")
		self.loc[4, 9] = Jiang("R")
		self.loc[5, 9] = Shi("R")
		self.loc[6, 9] = Xiang("R")
		self.loc[7, 9] = Ma("R")
		self.loc[8, 9] = Ju("R")

		self.loc[1, 7] = Pao("R")
		self.loc[7, 7] = Pao("R")

		self.loc[0, 6] = Bing("R")
		self.loc[2, 6] = Bing("R")
		self.loc[4, 6] = Bing("R")
		self.loc[6, 6] = Bing("R")
		self.loc[8, 6] = Bing("R")
	

	def move(self, x, y, dx, dy):
		self.Location[x, y].move(dx, dy)

	def move_check(self, i, j, color):
		if self.loc[i, j] != None and self.loc[i, j].color == color:
			return False
		else:
			return True

