# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.services.batting_service import BattingService
from app.services.pitching_service import PitchingService
from app.services.player_service import PlayerService
from app.services.league_context_service import LeagueContextService

batting_service = BattingService()
pitching_service = PitchingService()
player_service = PlayerService()
league_context_service = LeagueContextService()

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.batting import bp as batting_bp
    from app.routes.pitching import bp as pitching_bp
    from app.routes.players import bp as players_bp
    from app.routes.league_context import bp as league_context_bp

    app.register_blueprint(batting_bp)
    app.register_blueprint(pitching_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(league_context_bp)

    return app