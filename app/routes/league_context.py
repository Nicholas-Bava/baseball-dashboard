# app/routes/league_context.py
from flask import Blueprint, jsonify, request
from app import league_context_service

bp = Blueprint("league_context", __name__, url_prefix="/api/league-context")

@bp.route("/batting")
def batting_context():
    stat = request.args.get("stat", "homeRuns")
    # seasons comes in as comma separated string e.g. "2022,2023,2024"
    seasons_param = request.args.get("seasons", "")

    if not seasons_param:
        return jsonify({"error": "seasons parameter required"}), 400

    # Convert "2022,2023,2024" to [2022, 2023, 2024]
    try:
        seasons = [int(s) for s in seasons_param.split(",")]
    except ValueError:
        return jsonify({"error": "Invalid seasons format"}), 400

    data = league_context_service.get_batting_context(stat, seasons)
    return jsonify(data)

@bp.route("/rankings/batting")
def batting_rankings():
    player_id = request.args.get("playerId", type=int)
    season = request.args.get("season", type=int)

    if not player_id or not season:
        return jsonify({"error": "playerId and season required"}), 400

    data = league_context_service.get_player_rankings(player_id, season)
    return jsonify(data)


@bp.route("/distribution")
def stat_distribution():
    stat = request.args.get("stat", "avg")
    seasons_str = request.args.get("seasons", "")
    seasons = [int(s) for s in seasons_str.split(",") if s]

    if not seasons:
        return jsonify({"error": "seasons required"}), 400

    data = league_context_service.get_stat_distribution(stat, seasons)
    return jsonify(data)