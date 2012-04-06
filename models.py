def tilePlayed(self, board):
	for i in range(-1, 2):
		for j in range(-1, 2):
			if i == 0 and j == 0:
				print("Center")
			else:
				if board.tiles[i][j].value == self.value:
					self.touching += 1
				else:
					print("Not touching %s, %s" % (i,j))
				

class Player():

	def __init__(self):
		self.points = 0
		self.name = raw_input("Name: ")

class Board():

	tiles = []

	def __init__(self, width, height):
		self.width = width
		self.height = height
		for y in range(0, self.height):
			row = []
			for x in range(0, self.width):
				new_tile = Tile(x,y)
				new_tile.onChange.__iadd__(tilePlayed)
				row.append(new_tile)
			self.tiles.append(row)

	def printBoard(self):
		for x in range(0, self.width):
			row = ''
			for y in range(0, self.height):
				row += '%s ' % self.tiles[y][x].getValue()
			print(row)

	def playSpot(self, x, y):
		if not self.tiles[x][y].occupied():
			self.tiles[x][y].increment()
			self.tiles[x][y].onChange.fire(self.tiles[x][y],self)
			return True
		return False



class Tile():

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.value = 0
		self.touching = 0
		self.onChange = EventHook()

	def getValue(self):
		return self.value

	def increment(self):
		self.value += 1

	def occupied(self):
		if self.value > 0:
			return True
		return False

	def clear(self):
		self.value = 0

class EventHook(object):

	def __init__(self):
		self.__handlers = []

	def __iadd__(self, handler):
		self.__handlers.append(handler)
		return self

	def __isub__(self, handler):
		self.__handlers.remove(handler)

	def fire(self, *args, **keywargs):
		for handler in self.__handlers:
			handler(*args, **keywargs)

	def clearObjectHandlers(self, inObject):
		for theHandler in self.__handlers:
			if theHandler.im_self == inObject:
				self -= theHandler