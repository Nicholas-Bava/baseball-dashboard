# app/routes/players.py
from flask import Blueprint, jsonify, request
from app import player_service

bp = Blueprint("players", __name__, url_prefix="/api/players")

@bp.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Missing search query"}), 400
    results = player_service.search(query)
    return jsonify(results)

@bp.route("/<string:player_name>")
def player_profile(player_name):
    data = player_service.get_player_profile(player_name)
    if not data["batting"] and not data["pitching"]:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(data)