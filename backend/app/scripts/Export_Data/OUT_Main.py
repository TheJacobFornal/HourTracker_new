from app.scripts.Export_Data import OUT_DB


def process_list(projects):
    project_details_list = []

    for project in projects:
        project = OUT_DB.get_project_details(project)
        if project:
            project_details_list.append(project)

    return project_details_list


def projects_details():
    projects = OUT_DB.get_projects_list()
    return process_list(projects)


def serach_project(search_term):
    projects = OUT_DB.search_projects(search_term)
    return process_list


if __name__ == "__main__":
    main()
