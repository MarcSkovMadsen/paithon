"""Helper functionality for creating components"""
from typing import Dict, Tuple

import panel as pn

LAYOUT_PARAMETERS = {
    "background",
    "height",
    "width",
    "sizing_mode",
    "scroll",
    "min_height",
    "max_height",
    "min_width",
    "max_width",
}


def get_theme() -> str:
    """Returns the current theme: 'default' or 'dark'

    Returns:
        str: The current theme
    """
    args = pn.state.session_args
    if "theme" in args and args["theme"][0] == b"dark":
        return "dark"
    return "default"


def extract_layout_parameters(params: Dict) -> Tuple[Dict, Dict]:
    """Returns params, layout_params

    Args:
        params (Dict): Parameters provided to component

    Returns:
        Tuple[Dict, Dict]: params, layout_params
    """
    layout_params = {}
    non_layout_params = {}
    for key, val in params.items():
        if key in LAYOUT_PARAMETERS:
            layout_params[key] = val
        else:
            non_layout_params[key] = val
    if "name" in params:
        non_layout_params["name"] = layout_params["name"] = params["name"]
    return non_layout_params, layout_params
