from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from company import *

app = Flask(__name__)

_board = None

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/new', methods=['POST'])
def new_game():
	error = None
	if request.method == 'POST':
		try: 
			players = [Player(request.form['player1']), Player(request.form['player2'])]
			try:
				height = int(request.form['height'])
				width = int(request.form['width'])
			except ValueError:
				print("Bad value")
			board = Board(players, width, height)
			board.print_board()
		except KeyError:
			print("Bad")

		return render_template('game.html')
	else:
		error = 'Wrong'

@app.route('/play/<tile>')
def play():
	play_tile(tile)

if __name__ == '__main__':
	app.debug = True
	app.run()
