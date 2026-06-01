# app/routes/statcast.py
from flask import Blueprint, jsonify, request
from app import statcast_service

bp = Blueprint("statcast", __name__, url_prefix="/api/statcast")

@bp.route("/zones")
def player_zones():
    player_id = request.args.get("playerId", type=int)
    season = request.args.get("season", type=int)

    if not player_id or not season:
        return jsonify({"error": "playerId and season required"}), 400

    data = statcast_service.get_player_zone_data(player_id, season)

    if not data:
        return jsonify({"error": "No zone data found"}), 404

    return jsonify(data)

@bp.route("/season")
def player_season():
    player_id = request.args.get("playerId", type=int)
    season = request.args.get("season", type=int)

    if not player_id or not season:
        return jsonify({"error": "playerId and season required"}), 400

    data = statcast_service.get_player_season_statcast(player_id, season)

    if not data:
        return jsonify({"error": "No Statcast data found"}), 404

    return jsonify(data)