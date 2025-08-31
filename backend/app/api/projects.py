# projects.py
from flask import Blueprint, jsonify

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/", methods=["GET"])
def get_projects():
    projects = [{"id": 1, "name": "Project 1"}, {"id": 2, "name": "Project 2"}]
    return jsonify(projects)
