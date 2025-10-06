from flask import Blueprint, request, jsonify, current_app, abort
from app import db
from models import User, Word, Game, Guess, UserWord
from schemas import UserSchema, WordSchema, GameSchema, GuessSchema, UserWordSchema
import json

api_bp = Blueprint('api', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
word_schema = WordSchema()
words_schema = WordSchema(many=True)
game_schema = GameSchema()
games_schema = GameSchema(many=True)
guess_schema = GuessSchema()
guesses_schema = GuessSchema(many=True)
userword_schema = UserWordSchema()
userwords_schema = UserWordSchema(many=True)

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@api_bp.route('/users', methods=['POST'])
def create_user():
    body = request.get_json() or {}
    username = (body.get('username') or '').strip()
    email = (body.get('email') or '').strip().lower()

    if not username or not email:
        return jsonify({'error': 'username and email required'}), 400
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'invalid email format'}), 400
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'username or email already exists'}), 409

    u = User(username=username, email=email)
    db.session.add(u)
    db.session.commit()
    return user_schema.jsonify(u), 201

@api_bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return users_schema.jsonify(users), 200

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = User.query.get_or_404(user_id)
    return user_schema.jsonify(u), 200

@api_bp.route('/words', methods=['POST'])
def create_word():
    body = request.get_json() or {}
    text = (body.get('text') or '').strip().lower()
    difficulty = (body.get('difficulty') or 'medium').strip().lower()

    if not text or len(text) < 3:
        return jsonify({'error': 'word text must be at least 3 letters'}), 400
    if not text.isalpha():
        return jsonify({'error': 'word must contain letters only'}), 400
    if Word.query.filter_by(text=text).first():
        return jsonify({'error': 'word already exists'}), 409

    w = Word(text=text, difficulty=difficulty)
    db.session.add(w)
    db.session.commit()
    return word_schema.jsonify(w), 201

@api_bp.route('/words', methods=['GET'])
def list_words():
    length = request.args.get('length', type=int)
    if length:
        words = Word.query.filter(db.func.length(Word.text) == length).all()
    else:
        words = Word.query.all()
    return words_schema.jsonify(words), 200

@api_bp.route('/words/<int:word_id>', methods=['GET'])
def get_word(word_id):
    w = Word.query.get_or_404(word_id)
    return word_schema.jsonify(w), 200

@api_bp.route('/users/<int:user_id>/bookmark/<int:word_id>', methods=['POST'])
def bookmark_word(user_id, word_id):
    body = request.get_json() or {}
    note = (body.get('note') or '').strip()
    user = User.query.get_or_404(user_id)
    word = Word.query.get_or_404(word_id)
    assoc = UserWord.query.filter_by(user_id=user_id, word_id=word_id).first()
    if not assoc:
        assoc = UserWord(user_id=user_id, word_id=word_id, note=note)
        db.session.add(assoc)
    else:
        assoc.note = note
    db.session.commit()
    return userword_schema.jsonify(assoc), 200

@api_bp.route('/users/<int:user_id>/bookmarks', methods=['GET'])
def user_bookmarks(user_id):
    user = User.query.get_or_404(user_id)
    bookmarks = user.bookmarked_words.all()
    return userwords_schema.jsonify(bookmarks), 200


@api_bp.route('/games', methods=['POST'])
def create_game():
    body = request.get_json() or {}
    user_id = body.get('user_id')
    length = body.get('length', 5)

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    try:
        length = int(length)
    except (ValueError, TypeError):
        return jsonify({'error': 'length must be an integer'}), 400

    user = User.query.get_or_404(user_id)

    word = Word.query.filter(db.func.length(Word.text) == length).order_by(Word.id).first()
    secret = word.text if word else 'apple'

    game = Game(user_id=user.id, secret=secret)
    db.session.add(game)
    db.session.commit()
    obj = game_schema.dump(game)     
    obj.pop('secret', None)
    return jsonify(obj), 201

@api_bp.route('/games', methods=['GET'])
def list_games():
    games = Game.query.all()
    out = []
    for g in games:
        obj = game_schema.dump(g)
        if g.status == 'in_progress':
            obj.pop('secret', None)
        out.append(obj)
    return jsonify(out), 200

@api_bp.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    g = Game.query.get_or_404(game_id)
    obj = game_schema.dump(g)
    if g.status == 'in_progress':
        obj.pop('secret', None)
    return jsonify(obj), 200

@api_bp.route('/games/<int:game_id>', methods=['PATCH'])
def patch_game(game_id):
    g = Game.query.get_or_404(game_id)
    body = request.get_json() or {}
    changed = False

    if 'status' in body:
        stat = body.get('status')
        if stat not in ['in_progress', 'won', 'lost']:
            return jsonify({'error': 'invalid status value'}), 400
        g.status = stat
        changed = True

    if 'max_guesses' in body:
        try:
            mg = int(body.get('max_guesses'))
            if mg < 1:
                return jsonify({'error': 'max_guesses must be >= 1'}), 400
            g.max_guesses = mg
            changed = True
        except (ValueError, TypeError):
            return jsonify({'error': 'max_guesses must be integer'}), 400

    if changed:
        db.session.commit()
    return game_schema.jsonify(g), 200

@api_bp.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    g = Game.query.get_or_404(game_id)
    db.session.delete(g)
    db.session.commit()
    return jsonify({'deleted': True}), 200

# Guesses create + read
@api_bp.route('/games/<int:game_id>/guesses', methods=['POST'])
def create_guess(game_id):
    g = Game.query.get_or_404(game_id)
    if g.status != 'in_progress':
        return jsonify({'error': 'game is finished'}), 400

    body = request.get_json() or {}
    guess_text = (body.get('guess') or '').strip().lower()

    if not guess_text or not guess_text.isalpha():
        return jsonify({'error': 'guess must be alphabetic and not empty'}), 400

    if len(guess_text) != len(g.secret):
        return jsonify({'error': f'guess must be {len(g.secret)} letters long'}), 400

    secret = g.secret.lower()
    result = [None] * len(guess_text)
    secret_letters = list(secret)

    for i, ch in enumerate(guess_text):
        if ch == secret[i]:
            result[i] = {'letter': ch, 'status': 'correct'}
            secret_letters[i] = None

    for i, ch in enumerate(guess_text):
        if result[i] is not None:
            continue
        try:
            idx = secret_letters.index(ch)
            result[i] = {'letter': ch, 'status': 'present'}
            secret_letters[idx] = None
        except ValueError:
            result[i] = {'letter': ch, 'status': 'absent'}

    gg = Guess(game_id=g.id, guess_text=guess_text, result_json=json.dumps(result))
    db.session.add(gg)
    db.session.commit()

    if all(p['status'] == 'correct' for p in result):
        g.status = 'won'
        db.session.commit()
    elif g.guesses.count() >= g.max_guesses:
        g.status = 'lost'
        db.session.commit()

    return jsonify({'guess_id': gg.id, 'result': result, 'game_status': g.status}), 201

@api_bp.route('/games/<int:game_id>/guesses', methods=['GET'])
def list_guesses(game_id):
    g = Game.query.get_or_404(game_id)
    guesses = g.guesses.order_by(Guess.created_at.asc()).all()
    out = []
    for gg in guesses:
        try:
            r = json.loads(gg.result_json) if gg.result_json else None
        except Exception:
            r = None
        out.append({'id': gg.id, 'guess_text': gg.guess_text, 'result': r, 'created_at': gg.created_at})
    return jsonify(out), 200

@api_bp.route('/seed_words', methods=['POST'])
def seed_words():
    """
    POST /api/seed_words with JSON { "words": ["crane","plane",... ] }
    Adds words if they do not exist. For testing/dev only.
    """
    body = request.get_json() or {}
    words = body.get('words') or []
    if not isinstance(words, list) or not words:
        return jsonify({'error': 'provide list of words'}), 400
    added = []
    for w in words:
        text = (w or '').strip().lower()
        if not text or not text.isalpha() or len(text) < 3:
            continue
        if not Word.query.filter_by(text=text).first():
            neww = Word(text=text)
            db.session.add(neww)
            added.append(text)
    db.session.commit()
    return jsonify({'added': added}), 201
