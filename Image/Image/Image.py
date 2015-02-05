#-*- coding: utf-8 -*-

class Image:

	def __init__(self, width=None, height=None, filename=None,
			background=None, pixels=None):
		assert(width is not None and (height is not None or
			pixels is not None) or (filename is not None))
		if filename is not None:
			self.load(filename)
		elif pixels is not None:
			self.width = width
			self.height = len(pixels)
			self.filename = filename
			self.meta = {}
			self.pixels = pixels
		else:
			self.width = width
			self.height = height
			self.filename = filename
			self.meta = {}
			self.pixels = create_array(width, height, background)


	"""
	工厂方法，采用classmethod装饰器，可以在Image类及其子类上直接调用
	"""
	@classmethod
	def from_file(Class, filename):
		return Class(filename=filename)

	@classmethod
	def create(Class, width, height, background=None):
		return Class(width=width, height=height, background=background)

	@classmethod
	def from_data(Class, width, pixels):
		return Class(width=width, pixels=pixels)


def create_array(width, height, background=None):
	if numpy is not None:
		if background is not None:
			return numpy.zeros(width * height, dtype=numpy.uint32)
		else:
			iterable = (background for _ in range(width * height))
			return numpy.fromiter(iterable, numpy.uint32)

	else:
		typecode = "I" if array .array("I").itemsize >= 4 else "L"
		background = (background if background is not None else
				ColorForName["transparent"])
		return array.array(typecode, [background] * width * height)


