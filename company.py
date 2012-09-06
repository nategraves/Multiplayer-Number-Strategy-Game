import json, uuid, jsonpickle

def uniqify(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

class Board():
	
	tiles = []

	def __init__(self, players=False, width=3, height=3):

		if players:
			self.players = players
		else:
			players = {"players": [Player("Player 1"), Player("Player 2")]}  

		self.width = int(width)
		self.height = int(height)
		self.total_tiles = self.width * self.height
		self.turn = 0
		self.id = "%s" % uuid.uuid4()
		self.last_played = None

		if len(self.tiles) is 0:
			for i in range(self.total_tiles):
				graph = []
				
				# Current tile isnt in the leftmost column
				if (i % self.width) is not 0:
					#Add the tile to the left
					graph.append(i-1)
				
				# Current tile isn't in the rightmost column
				if (i % self.width) is not (self.width - 1):
					#Add the tile to the right
					graph.append(i+1)

				# Current tile isn't in first row
				if i >= self.width:
					#Add the tile above
					graph.append(i - self.width)

				# Current tile isn't in the last row
				if i < (self.total_tiles - self.width):
					#Add the tile below
					graph.append(i + self.width)

				# Append the graph and initial value
				self.tiles.append({ 
					"value": 0,
					"graph": graph,
				})

	def play_tile(self, tile, player, increment=False, time_through=1):

		# Make sure some local vars are good to go
		time_through = time_through
		tile = int(tile)

		# Tile already has a value and it's not because of a match
		if int(self.tiles[tile]["value"]) is not 0 and increment is False:
			return False

		if time_through is 1:
			self.last_played = tile
			self.increment(tile)
		nodes = self.get_nodes(tile, [], True)

		if len(nodes) > 2:
			self.players[self.turn % 2].score += (len(nodes) * self.get_value(nodes[0]))
			for i in range(len(nodes)):
				if i == 0:
					self.increment(nodes[i])
					time_through = 1
				else:
					self.set_value(nodes[i], 0)
			time_through += 1
			self.play_tile(nodes[0], player, True, time_through)
		return True

	def get_nodes(self, current, nodes, first):
		
		nodes = nodes + [current]

		graph = self.tiles[current]["graph"]

		for each in graph:
			if each not in nodes:
				if self.get_value(each) == self.get_value(current):
 					newpath = self.get_nodes(each, nodes, False)
					if newpath: 
						nodes = nodes + newpath
		nodes = uniqify(nodes)
		return nodes

	def increment(self, tile):
		self.tiles[tile]["value"] += 1

	def get_value(self, tile):
		return self.tiles[int(tile)]["value"]

	def set_value(self, tile, value):
		self.tiles[tile]["value"] = value

	def serialize(self):
		players = []
		for each in self.players:
			players.append({"name": each.name, "score": each.score}) 
		board = json.dumps({ "id":self.id, "players":players, "tiles":self.tiles, "turn":self.turn })
		return board

class Tile():
	
	def __init__(self, id):
		self.value = 0
		self.id = id

	def increment(self):
		self.value += 1

class Player():

	def __init__(self, name=None):
		self.score = 0
		if name:
			self.name = name
		else:
			self.name = "Player"

