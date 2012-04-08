# 00,01,02,03,
# 04,05,06,07,
# 08,09,10,11
# 12,13,14,15

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

	def __init__(self):
		for each in range(0,16):
			self.tiles.append(Tile(each))

	def print_board(self):
		for each in self.tiles:
			print("%s" % (each.id))
			if (each.id + 1) % 4 == 0:
				print('')

	def get_nodes(self, start, nodes=[]):
		nodes = nodes + [start]
		if not self.graph.has_key(start):
			return None
		for node in self.graph[start]:
			print("Working on %s.................." % node)
			print("Nodes: %s" % self.graph[start])
 			if node not in nodes:
 				print("%s not in %s" % (node, nodes))
				if self.tiles[node].value == self.tiles[start].value:
					newpath = self.get_nodes(node, nodes)
					if newpath: return newpath
		return nodes

	def increment(self, tile):
		self.tiles[tile].value += 1


class Tile():
	
	def __init__(self, id):
		self.value = 0
		self.id = id

	def increment(self):
		self.value += 1
