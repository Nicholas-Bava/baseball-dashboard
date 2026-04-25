# app/routes/pitching.py
from flask import Blueprint, jsonify, request
from app import pitching_service

bp = Blueprint("pitching", __name__, url_prefix="/api/pitching")

@bp.route("/leaderboard")
def leaderboard():
    stat = request.args.get("stat", "era")
    season = request.args.get("season", None, type=int)
    limit = request.args.get("limit", 25, type=int)
    df = pitching_service.get_leaderboard(stat, season, limit)
    return jsonify(df.to_dict(orient="records"))

@bp.route("/player/<string:player_name>")
def player_career(player_name):
    data = pitching_service.get_player_career(player_name)
    if not data:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(data)

@bp.route("/season/<int:year>")
def season_summary(year):
    data = pitching_service.get_season_summary(year)
    if not data:
        return jsonify({"error": "Season not found"}), 404
    return jsonify(data)