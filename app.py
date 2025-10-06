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

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///wordle_phase4.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)
    CORS(app) 

    with app.app_context():     
        import models 
        from routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')

        db.create_all()

    @app.route('/')
    def index():
        return jsonify({'message': 'Wordle Phase4 API — backend only'}), 200

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
