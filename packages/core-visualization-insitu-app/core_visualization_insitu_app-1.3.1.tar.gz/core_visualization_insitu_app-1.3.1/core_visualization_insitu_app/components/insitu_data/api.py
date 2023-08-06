"""
InsSituData api
"""

from core_visualization_insitu_app.components.insitu_data.models import InSituData


def get_all_data():
    """Return the list of all the insitu_data

    Returns:

    """
    return InSituData.get_all_data()


def get_data(project, build, part):
    """Get all insitu_data objects having the same project, build and part.
    Should be 7 of them (3 tabs for data_name builds command and 2 tabs for data_name melt pool and layer wise)

    Args:
        project:
        build:
        part:

    Returns:

    """
    return InSituData.get_data(project, build, part)


def get_data_by_tab_name(data, data_name, tab):
    """Return a single insitu_data object

    Args:
        data: dict of selected project, build and part
        data_name: Window name
        tab: tab position

    Returns:

    """

    project = data["project"]
    build = data["build"]
    part = data["part"]
    return InSituData.get_data_by_tab_name(project, build, part, data_name, tab)


def get_all_table():
    """Return list of list of all information in the table in the admin view for insitu data

    Returns:

    """
    insitu_data_objects = get_all_data()
    data_table = []
    for insitu_data_object in insitu_data_objects:
        total_layers = insitu_data_object.layer_numbers[-1]
        if total_layers > 0:
            data_name = insitu_data_object.data_name
            tab_number = insitu_data_object.tab
            data_line = [
                insitu_data_object.project,
                insitu_data_object.build,
                insitu_data_object.part,
                data_name,
                tab_number,
                total_layers,
            ]
            data_table.append(data_line)

    return data_table


def create_data(project, build, part, data_name, tab, images=None, layers=None):
    """Create an insitu object

    Args:
        project:
        build:
        part:
        data_name:
        tab:
        images:
        layers:

    Returns:

    """
    return InSituData.create_data(project, build, part, data_name, tab, images, layers)


def get_data_by_name_all_tabs(data, data_name):
    """Return 2 or 3 insitu objects (same project, build, part, data_name) and different tab

    Args:
        data:
        data_name:

    Returns:

    """
    project = data["project"]
    build = data["build"]
    part = data["part"]
    return InSituData.get_data_by_name_all_tabs(project, build, part, data_name)


def delete_all_data():
    """Delete all insitu_data objects

    Returns:

    """
    InSituData.delete_all_data()


def get_title(data, images, layers, layer_number=None):
    """Get the title of an image displayed. The title format is "Project, Build, Part, Layer number"

    Args:
        data: dict w/ selected project, build and part
        images:
        layers:
        layer_number:

    Returns:

    """
    if (len(images) > 0) and (len(layers) > 0):
        if layer_number is None:
            layer_number = layers[0]

        title = (
            data["project"]
            + ", "
            + data["build"]
            + ", "
            + data["part"]
            + ", "
            + " layer "
            + str(layer_number)
        )
    else:
        title = "No Data Available"

    return title


def reset_default_data(project, build, part):
    """Return the insitu_data objects with the according arguments,
    and put back the 1st layer as the one which is displayed

    Args:
        project:
        build:
        part:

    Returns:

    """

    return InSituData.reset_default_data(project, build, part)
