"""Visualization Insitu parser utils operations"""

import json
import core_explore_tree_app.components.data.query as query_database_api

from core_visualization_insitu_app.utils.dict import (
    get_list_inside_dict as utils_get_list,
)
from core_visualization_insitu_app.utils import dict as dict_utils

CQL_NAMESPACE = "http://siam.nist.gov/Database-Navigation-Ontology#"


def get_all_projects_list(navigation, template_id):
    """Return the list of the projects names tuples to put in the Django forms

    Args:
        navigation:
        template_id:

    Returns:

    """
    projects_id_tuples = get_projects(navigation, template_id)
    all_projects_list = []
    for project_tuple in projects_id_tuples:
        all_projects_list.append(project_tuple[0])
    return all_projects_list


def get_projects(navigation, template_id):
    """Get all the existing projects from the database

    Args:
        navigation:
        template_id:

    Returns: list of tuples. Each tuple is a project written twice to be consistent with form syntax

    """
    # Get the filter related to the projects
    owl_node_project = CQL_NAMESPACE + "AMProject"
    navigation_projects = navigation.get_by_name(owl_node_project)

    projects_id = []

    # All the navigation objects are identical so it is enough to get the information we need from the first one
    if (
        "filter" in navigation_projects[0].options
        and navigation_projects[0].options["filter"] is not None
    ):
        project_filter = navigation_projects[0].options["filter"]
    if (
        "projection" in navigation_projects[0].options
        and navigation_projects[0].options["projection"] is not None
    ):
        project_projection = navigation_projects[0].options["projection"]

    if not (project_filter and project_projection is None):
        projects = query_database_api.execute_query(
            template_id, [project_filter], project_projection
        )
        for project in projects:
            project_id = dict_utils.get_dict_value(project.dict_content, "projectID")
            if project_id not in projects_id:
                projects_id.append(project_id)

    projects_id_tuples = []
    for project_id in projects_id:
        projects_id_tuples.append((project_id, project_id))

    return projects_id_tuples


def get_builds_from_projectname(template_id, project_name):
    """Return build tuples, a list of tuples. Each tuple is a build.

    Returns:

    """

    # Query the database
    build_path = "dict_content.amBuildDB.amBuild.generalInfo.buildID"
    project_filter = {
        "dict_content.amBuildDB.amBuild.projectID": project_name
    }  # project}
    projection = {build_path: 1}
    builds = query_database_api.execute_query(
        template_id, [json.dumps(project_filter)], json.dumps(projection)
    )

    builds_names = []

    # get builds names
    for build_result in builds:
        build_dict = build_result.dict_content
        # list of dict with buildID as a key and its value (build name)
        build_list = utils_get_list(build_path, build_dict)
        # Create a list with only the builds names
        for build in build_list:
            builds_names.append(build["buildID"])

    return builds_names


def get_parts_from_buildname(template_id, build_name):
    """Return part tuples, a list of tuples. Each tuple is a part.

    Returns:

    """
    # Query the database
    part_path = "dict_content.amBuildDB.amBuild.parts.part"
    part_name_path = "dict_content.amBuildDB.amBuild.parts.part.partName"
    part_id_path = "dict_content.amBuildDB.amBuild.parts.part.partID"
    build_filter = {"dict_content.amBuildDB.amBuild.generalInfo.buildID": build_name}
    projection = {part_path: 1}
    parts = query_database_api.execute_query(
        template_id, [json.dumps(build_filter)], json.dumps(projection)
    )
    # list of dicts
    parts_id_and_names = []
    # set parts objects
    for part_result in parts:
        # dict content of the Data
        part_dict = part_result.dict_content
        # Get the part key and its values
        parts_list = utils_get_list(part_path, part_dict)
        # list of dicts with 1 key/value (part as a key) and a dict as its value
        # from the dict only get the keys that correspond to "part"
        # Split the list
        for part_dict in parts_list:
            # Take the several partID and associated name
            for elt in part_dict["part"]:
                elt = dict(elt)
                part_name = elt["partName"]
                part_id = elt["partID"]
                parts_id_and_names.append(part_name)

    return parts_id_and_names
