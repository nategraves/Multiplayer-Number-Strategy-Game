import sqlite3, time, datetime
from flask import Flask, render_template, request, jsonify
from company import *

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

app = Flask(__name__)
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
			_board = Board(player, 50, 50)
		except KeyError:
			print("Bad")
		return jsonify(board=_board.serialize())
	else:
		return render_template('index.html')

@app.route('/play/<tile>')
def play():
	play_tile(tile)

if __name__ == '__main__':
	app.debug = True
	app.run()
	board = Board()
