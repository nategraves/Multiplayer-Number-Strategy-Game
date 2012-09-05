import sqlite3, time, datetime
from flask import g, Flask, render_template, redirect, request, jsonify, url_for
from company import *

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
	return render_template('index.html')

@app.route('/play/', defaults={'tile': None}, methods=['POST', 'GET'])
@app.route('/play/<int:tile>/')
def play(tile):
	if request.method == 'POST':
		try: 
			players = [Player(request.form['player1']), Player('player2')]
			board = Board(players, request.form['width'], request.form['width'])
			print(board.serialize_board())
			return render_template('board.html', width=board.width, height=board.height, board=board )
		except KeyError:
			return redirect(url_for('index'))
	elif tile:
		board.turn += 1
		board.play_tile(int(tile), board.players[0])
		return render_template('board.html', width=board.width, height=board.height, board=board)
	else:
		board = Board([Player("Nate"), Player("Lev")], 4, 4)
		print(board.serialize_board())
		return render_template('board.html', width=board.width, height=board.height, board=board)


if __name__ == '__main__':
	app.debug = True
	app.run()
