from flask import Blueprint, jsonify

# Create a Blueprint for activities
activities_bp = Blueprint("activities", __name__)


# Sample route for activities
@activities_bp.route("/", methods=["GET"])
def get_activities():
    # In a real scenario, you'd query your database or model here
    activities = [
        {"id": 1, "name": "Activity 1"},
        {"id": 2, "name": "Activity 2"},
    ]
    return jsonify(activities)
