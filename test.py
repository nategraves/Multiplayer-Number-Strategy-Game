from flask import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite:////tmp/board.db
db = SQLAlchemy(app)

class Board(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	width = db.Column(db.Integer)
	height = db.Column(db.Integer)

	def __repr__(self):
		return '<Board %r>' % self.id

	@property
	def total_tiles(self):
		return self.width * self.height

class Tile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Integer)
	graph = db.Column(db.String(7))
	board = db.Column(db.Integer, db.ForeignKey('board.id'))
	board = db.relationship('Board', backref=db.backref('board', lazy='dynamic'))

	def __init__(self, board):
		self.value = 0
		self.board = board
