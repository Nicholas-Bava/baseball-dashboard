# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.services.batting_service import BattingService
from app.services.pitching_service import PitchingService
from app.services.player_service import PlayerService

batting_service = BattingService()
pitching_service = PitchingService()
player_service = PlayerService()

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.batting import bp as batting_bp
    from app.routes.pitching import bp as pitching_bp
    from app.routes.players import bp as players_bp

    app.register_blueprint(batting_bp)
    app.register_blueprint(pitching_bp)
    app.register_blueprint(players_bp)

    return app