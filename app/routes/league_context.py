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