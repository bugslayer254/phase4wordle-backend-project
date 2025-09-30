from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os

db = SQLAlchemy()
ma = Marshmallow()

def create_app(test_config=None):
    app = Flask(__name__, static_folder=None)

    # default config (sqlite for simplicity)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///wordle_phase4.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # init extensions
    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)
    CORS(app)  # enable CORS for all routes

    with app.app_context():        # register models and routes (ensure import after init)
        import models  # registers models with SQLAlchemy
        from routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')

        db.create_all()

    @app.route('/')
    def index():
        return jsonify({'message': 'Wordle Phase4 API — backend only'}), 200

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
