import sqlite3, time, datetime
from flask import Flask, render_template, request, jsonify, url_for
from company import *

app = Flask(__name__)

#def connect_db():
#	return sqlite3.connect(app.config['DATABASE'])

#def init_db():
#	with closing(connect_db()) as db:
#		with app.open_resource('schema.sql') as f:
#			db_cursor().executescript(f.read())
#		db.commit()

# DB Configuration
DATABASE = '/tmp/threes.db'
DEBUG = True
SECRET_KEY = 'n1a9t8e1'
USERNAME = 'threes'
PASSWORD = 'fjru48.fj'
_board = None

#app.config.from_object(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
	error = None
	_board = None
	if request.method == 'POST':
		try: 
			form_data = request.form['player']
			current_time = int(time.mktime(datetime.datetime.now().timetuple()))
			player = Player('%s %s' % (form_data, current_time))
			_board = Board(player, 3, 3)
		except KeyError:
			print("Bad")
		return jsonify(board=_board.serialize())
	else:
		return render_template('index.html')

@app.route('/play/')
def play():
	return render_template('board.html', width=_board.width, height=_board.height, board=_board )

@app.route('/play/<tile>/')
def play_web_tile(tile=False):
	if(tile):
		_board.turn += 1
		_board.play_tile(int(tile), _board.players[0])
	return render_template('board.html', width=_board.width, height=_board.height, board=_board)


if __name__ == '__main__':
	app.debug = True
	players = [Player('Player 1'), Player('Player 2')]
	_board = Board(players, 3, 3)
	app.run()
