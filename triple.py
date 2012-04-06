from models import Player, Board, Tile	

	

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

print("\r\nBoard: ")
board = Board(5,5)
board.playSpot(0,0)
board.playSpot(1,0)
print(board.tiles[0][0].touching)
print(board.tiles[1][0].touching)
board.printBoard()

#print("Player 1")
#player1 = Player()

#playGame(board, players)
