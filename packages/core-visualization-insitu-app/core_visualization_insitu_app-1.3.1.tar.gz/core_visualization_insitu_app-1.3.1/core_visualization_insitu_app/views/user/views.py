""" Insitu Visualization app user views
"""
import logging

from django.core.cache import caches
from django.http import HttpResponseBadRequest

import core_explore_tree_app.components.query_ontology.api as query_ontology_api
from core_explore_tree_app.components.navigation.api import (
    create_navigation_tree_from_owl_file,
)
from core_main_app.commons import exceptions
from core_main_app.utils.rendering import render
from core_visualization_insitu_app.utils.operations import (
    get_parts_from_buildname,
    get_builds_from_projectname,
    get_all_projects_list,
)
from core_visualization_insitu_app.components.insitu_data import (
    operations as data_operations,
)


from core_visualization_insitu_app.views.user.forms import (
    SelectProjectDropDown,
    SelectBuildDropDown,
    SelectPartDropDown,
)

logger = logging.getLogger(__name__)

navigation_cache = caches["navigation"]


def index(request):
    """Visualization Insitu app initial page

    Args:
        request:

    Returns:

    """
    error = None
    active_ontology = None

    try:
        # Set up the needed explore tree related objects to get the queries
        # get the active ontology
        active_ontology = query_ontology_api.get_active()

    except exceptions.DoesNotExist:

        error = {
            "error": "An Ontology should be active to explore. Please contact an admin."
        }

    if error is None:
        try:
            # Get the active ontology's ID
            template_id = active_ontology.template.id
            nav_key = active_ontology.id

            # get the navigation from the cache
            if nav_key in navigation_cache:
                navigation = navigation_cache.get(str(nav_key))
            else:
                # create the navigation
                navigation = create_navigation_tree_from_owl_file(
                    active_ontology.content
                )
                navigation_cache.set(
                    nav_key, navigation
                )  # navigation_cache.set(template_id, navigation)

            # Get the existing projects from the navigation
            projects = get_all_projects_list(navigation, template_id)
            projects_tuples = []
            for project in projects:
                projects_tuples.append(tuple([project, project]))

            select_project = SelectProjectDropDown()
            select_project.fields["projects"].choices = projects_tuples

            # We take the first project as a default for the projects form
            default_project = projects_tuples[0][0]

            # Get builds depending on default active project
            builds = get_builds_from_projectname(template_id, default_project)

            select_build = SelectBuildDropDown()
            builds_tuples = []
            for build in builds:
                builds_tuples.append(tuple([build, build]))
            select_build.fields["builds"].choices = builds_tuples

            # We take the first build as a default for the builds form
            default_build = builds_tuples[0][0]

            # Get parts depending on default active project
            parts = get_parts_from_buildname(template_id, default_build)

            select_part = SelectPartDropDown()

            parts_tuples = []
            for part in parts:
                parts_tuples.append(tuple([part, part]))

            select_part.fields["parts"].choices = parts_tuples
            # Data information

            # We take the first part as a default for the parts form
            default_part = parts_tuples[0][0]
            data_information = data_operations.query_data_information(
                template_id, default_build, default_part
            )
        except exceptions.DoesNotExist as e_does_not_exist:
            error = {"error": str(e_does_not_exist)}
        except Exception as e:
            error = {"error": str(e)}
    if error:
        context = error
    else:

        selected_layers = {
            "build-command": int(1),
            "melt-pool": int(1),
            "layer-wise": int(1),
            "xray-computed-tomography": int(1),
        }

        current_session = request.session.session_key
        # Set the current layers tab numbers for the active session
        request.session["selected_layers"] = selected_layers

        context = {
            "projects": select_project,
            "builds": select_build,
            "parts": select_part,
            "total_layers": data_information["total_layers"],
            "build_location": data_information["build_location"],
            "layer_thickness": data_information["layer_thickness"],
        }
    assets = {
        "css": [
            "css/landing.css",
            "core_visualization_insitu_app/common/css/loading_background.css",
        ],
        "js": [
            {
                "path": "core_visualization_insitu_app/user/js/load_data_information.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/js/select_build_form.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/js/tab_manager.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/js/select_part_form.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/js/select_project_form.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/js/access_layer_number.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/js/display_blobs.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/libs/threejs_library.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/libs/stl_controls.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/libs/stl_loader.js",
                "is_raw": False,
            },
            {
                "path": "core_visualization_insitu_app/user/js/load_data_information_raw.js",
                "is_raw": True,
            },
            {
                "path": "core_visualization_insitu_app/user/js/select_build_form_raw.js",
                "is_raw": True,
            },
            {
                "path": "core_visualization_insitu_app/user/js/select_part_form_raw.js",
                "is_raw": True,
            },
            {
                "path": "core_visualization_insitu_app/user/js/select_project_form_raw.js",
                "is_raw": True,
            },
            {
                "path": "core_visualization_insitu_app/user/js/access_layer_number_raw.js",
                "is_raw": True,
            },
            {
                "path": "core_visualization_insitu_app/user/js/display_blobs_raw.js",
                "is_raw": True,
            },
        ],
    }

    return render(
        request,
        "core_visualization_insitu_app/user/visualization_index.html",
        assets=assets,
        context=context,
    )
