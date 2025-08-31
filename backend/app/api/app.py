from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS to allow cross-origin requests
from app.scripts.Export_Data import OUT_DB
from app.scripts.Export_Data import OUT_Main

app = Flask(__name__)

CORS(app)

@app.route("/api/projects/search", methods=["POST"])
def search_project():
    data = request.get_json()  # <-- this gets the JSON payload

    # Example: access values
    users = data.get("users", [])
    status = data.get("status")
    leader = data.get("leader")
    date_from = data.get("date_from")
    date_to = data.get("date_to")
    search = data.get("search", "")

    print(users, status, leader, date_from, date_to, search, flush=True)

    results = [
        {
            "id": "IX_215323",
            "hours": 1,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 2,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215323",
            "hours": 1,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 2,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
                {
            "id": "IX_215323",
            "hours": 5100,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },
        {
            "id": "IX_215324",
            "hours": 55,
            "user": "Eryk Królikowski",
            "dateRange": "2025-05-22 to 2025-07-31",
        },

    ]


    return jsonify(results)


@app.route("/api/project/header_info", methods=["POST"])
def header_info():
    data = request.get_json()  # <-- this gets the JSON payload

    # Example: access values
    project_name = data.get("project_name")



    results = [
        {
            "leader": "Eryk Królikowski",
            "dateFrom" : "2025-05-22",
            "dateTo" : "2025-07-31",
            "status" : "In Progress"
        }]


    return jsonify(results)

@app.route("/api/project/activities_details", methods=["POST"])
def activity_details():
    data = request.get_json() 

    project_name = data.get("project_name")
    date_from = data.get("date_from")
    date_to = data.get("date_to")

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

    return jsonify(results)

# Define the /api/project route
@app.route("/api/projects/test")
def project():

    #projects = OUT_Main.projects_details()
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

    leaders = ["Mariusz", "Rafal", "Zbyszek"]

    return leaders  # Return the data as JSON



    

if __name__ == "__main__":
    app.run(debug=True)
