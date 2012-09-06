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
			players = [Player(request.form['player1']), Player('player2')]
			board = Board(players, request.form['width'], request.form['width'])
			json_board = jsonpickle.encode(board)
			result = g.db.execute('insert into games (board) values (?)', [json_board])
			g.db.commit()
			return redirect(url_for('board', board_id=result.lastrowid))
		except KeyError:
			return redirect(url_for('index'))
	return render_template('index.html')

@app.route('/board/<int:board_id>/')
def board(board_id):
	if board_id is not None:
		response = query_db('select board from games where id=?', [int(board_id)])
		print("Board %s" % response[0].keys())
		board = jsonpickle.decode(response[0])
		return render_template('board.html', width=board.width, height=board.height, board=board)

@app.route('/play/<int:board_id>/<int:tile>/')
def play(board_id, tile):
	if board_id is not None and tile is not None:
		json_board = g.db.execute('select board from games where id=?', [board_id])
		board = jsonpickle.decode(json_board)
		board.turn += 1
		board.play_tile(int(tile), board.players[0])
		json_board = jsonpickle.encode(board)
		result = g.db.execute('update games set board = ? where id = ?', [json_board, board_id])
		return redirect(url_for('board'), board_id=board_id)
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.debug = True
	app.run()
