from test import Board, Tile#,Player

def playTurn(board, response):
	x = int(response.partition(',')[2])
	y = int(response.partition(',')[0])
	print("Value at turn: %s" % board[x][y])

	#Can't play on an occupied tile
	
	accepted = checkOccupied(board, x, y)
	board = checkTouching(board, x, y)
	
	return accepted,board

def playGame(board, players):
	turn = 0
	game = True
	while game:
		
		accepted = True
		while accepted:
			printBoard(board)
			response = raw_input("%s's Turn (Enter play as x,y): " % players[turn][0])
			accepted,board = playTurn(board,response)
			if not accepted:
				print("That spot is already taken")
		turn += 1


def uniqify(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

board = Board()
board.tiles[2].increment()
board.tiles[5].increment()
board.tiles[10].increment()
board.tiles[14].increment()
board.print_board()
board.increment(6)
nodes = uniqify(board.get_nodes(6))
print(nodes)
#board = Board(5,10)
#board.printBoard()
#board.tiles[0][0].increment()
#board.printBoard()


#print("Player 1")
#player1 = Player()

#playGame(board, players)
