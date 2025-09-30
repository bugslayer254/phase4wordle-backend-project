from app import ma
from models import User, Word, Game, Guess, UserWord

class GuessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Guess
        include_fk = True
        load_instance = True
        fields = ("id", "game_id", "guess_text", "result_json", "created_at")

class GameSchema(ma.SQLAlchemyAutoSchema):
    guesses = ma.Nested(GuessSchema, many=True)
    class Meta:
        model = Game
        include_fk = True
        load_instance = True
        # By default Marshmallow will include all fields; we will remove 'secret' when needed on read
        fields = ("id", "user_id", "status", "created_at", "max_guesses", "guesses", "secret")

class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Word
        load_instance = True
        fields = ("id", "text", "difficulty", "created_at")

class UserWordSchema(ma.SQLAlchemyAutoSchema):
    word = ma.Nested(WordSchema)
    class Meta:
        model = UserWord
        include_fk = True
        load_instance = True
        fields = ("user_id", "word_id", "note", "created_at", "word")

class UserSchema(ma.SQLAlchemyAutoSchema):
    games = ma.Nested(GameSchema, many=True)
    bookmarked_words = ma.Nested(UserWordSchema, many=True)
    class Meta:
        model = User
        load_instance = True
        fields = ("id", "username", "email", "created_at", "games", "bookmarked_words")
