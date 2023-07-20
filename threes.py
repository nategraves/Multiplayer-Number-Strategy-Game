import sys
from company import Board, Player


def main():
    players = [Player(), Player()]
    try:
        width = int(input("How wide of a board would you like?\r\n"))
    except ValueError:
        print("Please enter a valid number")
    try:
        height = int(input("How tall of a board would you like?\r\n"))
    except ValueError:
        print("Please enter a valid number")
    board = Board(players, width, height)
    board.print_board()
    turn = 0
    game = True
    while turn < 50:
        played = False
        while not played:
            try:
                tile = int(input("What tile do you want to play, %s (0-%s)?\r\n" %
                           (board.players[turn % 2].name, board.total_tiles)))
                played = board.play_tile(tile, board.players[turn % 2], True)
            except ValueError:
                print("Please enter a valid number")
        turn += 1
    print("Game over!")
    sys.exit()


main()

'''
Some optional code to run to test stuff.

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
'''
