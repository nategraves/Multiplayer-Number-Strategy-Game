# 00,01,02,03,
# 04,05,06,07,
# 08,09,10,11
# 12,13,14,15

def uniqify(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

class Board():
	
	tiles = []

	def __init__(self, width=20, height=20):
		self.width = width
		self.height = height
		self.total_tiles = self.width * self.height

		for i in range(self.total_tiles):
			graph = []
			if (i + 1) < (self.total_tiles - 1):
				graph.append(i + 1)
			if (i - 1) >= 0:
				graph.append(i - 1)
			if (i + width) < (self.total_tiles - 1):
				graph.append(i + width)
			if (i - width) >= 0:
				graph.append(i - width)
			self.tiles.append({ 
				'value': 0,
				'graph': graph,
			})	

	def print_board(self):
		response = "\r\nBoard:\r\n"
		for (counter, each) in enumerate(self.tiles):
			response += "%s " % each['value']
			if (counter + 1) % self.width == 0:
				response += "\r\n"
		print(response)
		if len(self.players) > 1:
			print("%s: %s points | %s: %s points" % 
				(self.players[0].name, self.players[0].points, self.players[1].name, self.players[1].points))

	def get_nodes(self, current, nodes=[]):
		nodes = nodes + [current]
		for each in self.tiles[current]['graph']:
			if each not in nodes:
				if self.get_value(each) == self.get_value(current):
 					newpath = self.get_nodes(each, nodes)
					if newpath: nodes = nodes + newpath
		return uniqify(nodes)

	def increment(self, tile):
		self.tiles[tile]['value'] += 1
		print("Increment %s" % self.tiles[tile]['value'])

	def get_value(self, tile):
		return self.tiles[int(tile)]['value']

	def set_value(self, tile, value):
		self.tiles[tile]['value'] = value

	def play_tile(self, tile, player, increment=False):
		if self.get_value(tile) > 0 and increment:
			print("That tile is occupied.")
			return False

		if increment:
			self.increment(tile)
		nodes = self.get_nodes(tile)
		if len(nodes) > 2:
			player.points += (len(nodes) * self.get_value(nodes[0]))
			if increment:
				print("Played tile %s" % tile)
			for i in range(len(nodes)):
				if i == 0:
					self.increment(nodes[i])
				else:
					self.set_value(nodes[i], 0)
			self.play_tile(nodes[0], player, False)
		else:
			if increment:
				print("Played tile %s" % tile)
		if increment:
			self.print_board()

		return True

		@property
		def serialize(self):
			return {
				'player': self.players,
				'tiles': self.tiles
			}

class Tile():
	
	def __init__(self, id):
		self.value = 0
		self.id = id

	def increment(self):
		self.value += 1

class Player():

	def __init__(self, name=None):
		self.points = 0
		if name:
			self.name = name
		else:
			self.name = raw_input("Enter this player's name: \r\n")

