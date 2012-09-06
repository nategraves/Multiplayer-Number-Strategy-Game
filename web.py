# Do some importing stuff
import time, datetime, jsonpickle
from sqlite3 import dbapi2 as sqlite3
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

def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value)
				for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		try: 
			player1 = Player(request.form['player1'])
			player2 = Player(request.form['player2'])
			print(player1.name)
			print(player2.name)
			players = [player1, player2]
			board = Board(players, request.form['width'], request.form['width'])
			json_board = jsonpickle.encode(board)
			result = g.db.execute('insert into games (board) values (?)', [json_board])
			g.db.commit()
			return redirect(url_for('board', board_id=result.lastrowid, error=0))
		except KeyError:
			return redirect(url_for('index'))
	return render_template('index.html')

@app.route('/board/<int:board_id>/<int:error>/')
def board(board_id, error):
	
	if board_id is not None:

		# Get the board from the DB, decode it, pass it to the template
		response = query_db('select * from games where id=%s' % board_id)
		board = jsonpickle.decode(response[0]["board"])
		return render_template('board.html', width=board.width, height=board.height, board=board, id=response[0]["id"], error=error)

@app.route('/play/<int:board_id>/<int:tile>/', methods=['POST', 'GET'])
def play(board_id, tile):

	# Make a local var for board_id
	bid = int(board_id)

	if board_id is not None and tile is not None:

		# Get the board, decode it, increment the turn, play the tile
		response = query_db('select * from games where id=%s' % board_id)
		board = jsonpickle.decode(response[0]["board"])
		played = board.play_tile(int(tile), board.players[board.turn % len(board.players)])
		
		# Check to make sure the play was a success
		if played: 
			board.turn += 1
			error = 0
		else: 
			error = 1

		# Re-encode the updated board
		json_board = jsonpickle.encode(board)
		g.db.execute('update games set board = ? where id = ?', [json_board, board_id])
		g.db.commit()

		#Send the user back to the board
		return redirect(url_for('board', board_id=bid, error=error))
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.debug = True
	app.run()
