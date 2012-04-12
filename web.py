from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from company import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/new', methods=['POST'])
def new_game():
	error = None
	if request.method == 'POST':
		print(request.data)
		try: 
			width = request.form['width']
		except KeyError:
			print("Bad")
		#height = request.form['height']
		#player1 = request.form['player1']
		#player2 = request.form['player2']
		#print(width, height, player1, player2)
		return render_template('game.html')
	else:
		error = 'Wrong'

@app.route('/play/<tile>')
def play():
	play_tile(tile)

if __name__ == '__main__':
	app.debug = True
	app.run()
