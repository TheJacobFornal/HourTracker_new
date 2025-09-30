from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS to allow cross-origin requests
from app.scripts.Export_Data import OUT_DB
from app.scripts.Export_Data import OUT_Main
from app.scripts.Export_Data import Projects_Search
from app.scripts.Export_Data import Activity_Search

app = Flask(__name__)

CORS(app)


@app.route("/api/projects/search", methods=["POST"])
def search_project():
    data = request.get_json()

    users = data.get("users", [])
    status = data.get("status")
    leader = data.get("leader")
    date_from = data.get("date_from")
    date_to = data.get("date_to")
    date_order = data.get("date_sort")
    search = data.get("search", "")
    page = data.get("page", 1)
    page_size = data.get("page_size", 51)

    print(
        "pro",
        users,
        status,
        leader,
        date_from,
        date_to,
        date_order,
        search,
        page,
        page_size,
        flush=True,
    )
    restult_new, record_counter = Projects_Search.get_projects_list(
        users, status, leader, date_from, date_to, date_order, search, page, page_size
    )

    return jsonify({"projects": restult_new, "record_counter": record_counter})


@app.route("/api/project/header_info", methods=["POST"])
def header_info():
    data = request.get_json()  # <-- this gets the JSON payload

    # Example: access values
    project_name = data.get("project_name")

    results = [
        {
            "leader": "Eryk Królikowskiii",
            "dateFrom": "2025-05-22",
            "dateTo": "2025-07-31",
            "status": "In Progress",
        }
    ]

    return jsonify(results)


@app.route("/api/project/activities_details", methods=["POST"])
def activity_details():
    data = request.get_json()

    project_name = data.get("project_name")
    date_from = data.get("date_from")
    date_to = data.get("date_to")

    activity_list = Activity_Search.get_activity_list(project_name, date_from, date_to)

    print(project_name, date_from, date_to, flush=True)

    results = [
        {
            "activity": "Programowanie",
            "hours": 10,
            "users": {
                "Jakub Fornal": 10,
                "Jam Kowalski": 20,
                "Adrian Koks": 54,
            },
        },
        {
            "activity": "Testowanie",
            "hours": 8,
            "users": {
                "Eryk Królikowski": 5,
                "Jakub Fornal": 2,
                "Jam Kowalski": 6,
            },
        },
        {
            "activity": "Projektowanie",
            "hours": 12,
            "users": {
                "Anna Nowak": 7,
                "Adrian Koks": 3,
                "Jakub Fornal": 4,
            },
        },
        {
            "activity": "Analiza",
            "hours": 6,
            "users": {
                "Eryk Królikowski": 2,
                "Anna Nowak": 3,
                "Jam Kowalski": 1,
            },
        },
    ]

    return jsonify(activity_list)


# Define the /api/project route
@app.route("/api/projects/test")
def project():

    # projects = OUT_Main.projects_details()
    # print(project)
    # Example project data
    example_project1 = {
        "id": "IX_215323",
        "hours": 5100,
        "user": "Eryk Królikowski",
        "dateRange": "2025-05-22 to 2025-07-31",
    }

    example_project2 = {
        "id": "IX_215323",
        "hours": 55,
        "user": "Eryk Królikowski",
        "dateRange": "2025-05-22 to 2025-07-31",
    }

    return jsonify(example_project1, example_project2)  # Return the data as JSON


# Main route
@app.route("/get/leaders")
def index():
    print("Received request for leaders", flush=True)

    leaders = ["Mariusz", "Rafal", "Zbyszek"]

    return jsonify(leaders)  # Return the data as JSON


@app.route("/")
def home():
    print("Received request for home", flush=True)
    return "Hello, Flask API is running!"


if __name__ == "__main__":
    print("Starting Flask server...", flush=True)
    app.run(debug=True)
