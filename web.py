from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/new', methods=['POST', 'GET'])
def new_game():
	error = None
	if request.method == 'POST':
		pass #need to hand off to another method
		return('New game')
	else:
		return render_template('new.html')

if __name__ == '__main__':
	app.run(debug=True)
