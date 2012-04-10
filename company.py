# 00,01,02,03,
# 04,05,06,07,
# 08,09,10,11
# 12,13,14,15

def uniqify(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

class Board():
	
	graph = {
		0: [1,4],
		1: [0,2,5],
		2: [1,3,6],
		3: [2,7],
		4: [0,5,8],
		5: [1,4,6,9],
		6: [2,5,7,10],
		7: [3,6,11],
		8: [4,9,12],
		9: [5,8,10,13],
		10: [6,9,11,14],
		11: [7,10,15],
		12: [8,13],
		13: [9,12,14],
		14: [10,13,15],
		15: [11,14],
	}

	tiles = []

	def __init__(self, players):
		self.players = players
		for each in range(0,16):
			self.tiles.append(Tile(each))

	def print_board(self):
		response = ""
		for each in self.tiles:
			response += "%s " % each.value
			if (each.id + 1) % 4 == 0:
				response += "\r\n"
		print(response)
		print("%s: %s points | %s: %s points" % 
			(self.players[0].name, self.players[0].points, self.players[1].name, self.players[1].points))

	def get_nodes(self, current, nodes=[]):
		nodes = nodes + [current]
		for each in self.graph[current]:
			if each not in nodes:
				if self.get_value(each) == self.get_value(current):
 					newpath = self.get_nodes(each, nodes)
					if newpath: nodes = nodes + newpath
		return uniqify(nodes)

	def increment(self, tile):
		self.tiles[tile].value += 1

	def get_value(self, tile):
		return self.tiles[int(tile)].value

	def set_value(self, tile, value):
		self.tiles[tile].value = value

	def play_tile(self, tile, player, increment=False):
		if self.get_value(tile) > 0 and increment:
			print("That tile is occupied.")
			return False

		if increment:
			self.tiles[tile].value += 1
		nodes = self.get_nodes(tile)

		if len(nodes) > 2:
			player.points += (len(nodes) * (self.get_value(nodes[0]) - 1))
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

class Tile():
	
	def __init__(self, id):
		self.value = 0
		self.id = id

	def increment(self):
		self.value += 1

class Player():

	def __init__(self):
		self.points = 0
		self.name = raw_input("Enter this player's name: \r\n")

