#from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)

class UserWord(db.Model):
    __tablename__ = 'user_words'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), primary_key=True)
    note = db.Column(db.String(300), nullable=True)   
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    games = db.relationship('Game', backref='player', lazy='dynamic', cascade='all,delete-orphan')

    bookmarked_words = db.relationship('UserWord', backref='user', lazy='dynamic', cascade='all,delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), unique=True, nullable=False)
    difficulty = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('UserWord', backref='word', lazy='dynamic', cascade='all,delete-orphan')

    def __repr__(self):
        return f'<Word {self.text}>'

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    secret = db.Column(db.String(50), nullable=False)  
    status = db.Column(db.String(20), default='in_progress')  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    max_guesses = db.Column(db.Integer, default=6)

    guesses = db.relationship('Guess', backref='game', lazy='dynamic', cascade='all,delete-orphan')

    def __repr__(self):
        return f'<Game {self.id} user={self.user_id} status={self.status}>'

class Guess(db.Model):
    __tablename__ = 'guesses'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    guess_text = db.Column(db.String(50), nullable=False)
    result_json = db.Column(db.Text, nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Guess {self.guess_text} for game {self.game_id}>'
