import os
import sys

sys.path.append('/srv/www/tritina.com/tritina')

os.environ['PYTHON_EGG_CACHE'] = '/srv/www/tritina.com/.python-egg'

def application(environ, start_response):
    status = '200 OK'
    output = 'Kicking Off!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

import sqlite3, time, datetime
from flask import Flask, render_template, request, jsonify, url_for
from company import *

app = Flask(__name__)

# DB Configuration
DATABASE = '/tmp/threes.db'
DEBUG = True
SECRET_KEY = 'n1a9t8e1'
USERNAME = 'threes'
PASSWORD = 'fjru48.fj'
_board = None

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
    _board = Board(players, 6, 6)
    app.run()
