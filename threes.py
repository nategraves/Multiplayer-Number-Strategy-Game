from company import Board, Tile, Player

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

board = Board()

board.print_board()

#Get a 2 in the top right
board.play_tile(1, True)
board.play_tile(2, True)
board.play_tile(3, True)

#Get a two to the left
board.play_tile(1, True)
board.play_tile(6, True)
board.play_tile(2, True)

#Get a two below the corner spot
board.play_tile(6, True)
board.play_tile(11, True)
board.play_tile(7, True)

#Get another 3
board.play_tile(1, True)
board.play_tile(5, True)
board.play_tile(9, True)
board.play_tile(2, True)
board.play_tile(6, True)
board.play_tile(10, True)
board.play_tile(1, True)
board.play_tile(5, True)
board.play_tile(6, True)

#Third 3
board.play_tile(0, True)
board.play_tile(4, True)
board.play_tile(8, True)
board.play_tile(1, True)
board.play_tile(5, True)
board.play_tile(9, True)
board.play_tile(0, True)
board.play_tile(4, True)
board.play_tile(5, True)