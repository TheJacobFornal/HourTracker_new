from app.scripts.Export_Data_DB import OUT_DB
from app.scripts.Export_Data_DB import Activity_Search
import json


def process_list(
    projects,
):  # create a list of projects to Gallery view (name, lider, Total_Hours, Dates)
    project_details_list = []

    for project in projects:
        project = OUT_DB.get_project_details(project)
        if project:
            project_details_list.append(project)

    return project_details_list


def get_project_activities_user_json(project_name, date_from, date_to):
    # Get raw data from your existing functions
    activity_list = Activity_Search.get_activity_list(project_name, date_from, date_to)
    user_hour_list = OUT_DB.get_project_user_sumHour_list(project_name)

    # Create a structured dictionary
    final_dict = {"activities": activity_list, "users_summary": user_hour_list}

    # Convert to JSON string, with indentation for readability
    # json_output = json.dumps(final_dict, indent=4, ensure_ascii=False)

    return [activity_list, user_hour_list]


def projects_details():  # Header - Details in Project Page
    projects = OUT_DB.get_projects_list()
    return process_list(projects)


def serach_project(search_term):  # Search Bar in Gallery View
    projects = OUT_DB.search_projects(search_term)
    return process_list(projects)


def get_activity_hours_per_user(project_name: str):
    data = OUT_DB.get_activity_hours_per_user(project_name)
    return data


def get_data_to_Export_Excel(project_name):  # Export to Excel Data
    data = OUT_DB.get_activity_hours_per_user(project_name)
    return data


if __name__ == "__main__":
    print("Ale szef ;)")

    project = "250403-CF"

    data = get_data_to_Export_Excel(project)

    print(json.dumps(data, indent=4, ensure_ascii=False))
