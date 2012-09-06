# Do some importing stuff
import sqlite3, time, datetime
from contextlib import closing
from company import *
from flask import Flask, render_template, redirect, request, jsonify, url_for, g, abort, flash


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('settings', silent=True)

DATABASE = 'tritina.db'
DEBUG = True
SECRET_KEY = 'w1hallg4a1r'
USERNAME = 'admin'
PASSWORD = 'fjru48.fj'

def connect_db():
	return sqlite3.connect(DATABASE)

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

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
			json_board = board.serialize()
			print(json_board)
			#g.db.execute('insert into games (board) values (?)', [json_board,])
    		#g.db.commit()
			return render_template('board.html', width=board.width, height=board.height, board=board )
		except KeyError:
			return redirect(url_for('index'))
	elif tile:
		board.turn += 1
		board.play_tile(int(tile), board.players[0])
		return render_template('board.html', width=board.width, height=board.height, board=board)
	else:
		board = Board([Player("Nate"), Player("Lev")], 4, 4)
		print(board.serialize())
		return render_template('board.html', width=board.width, height=board.height, board=board)


if __name__ == '__main__':
	app.debug = True
	app.run()
