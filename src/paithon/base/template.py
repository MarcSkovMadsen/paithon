"""Functionality to easily create templates"""
import panel as pn

pn.extension(sizing_mode="stretch_width")

ACCENT_COLOR = "#0072B5"
DEFAULT_PARAMS = {
    "site": "🧠 Paithon",
    "accent_base_color": ACCENT_COLOR,
    "header_background": ACCENT_COLOR,
}


def fastlisttemplate(**params):
    """Returns a Paithon version of the FastListTemplate

    Returns:
        [FastListTemplate]: A FastListTemplate
    """
    params = {**DEFAULT_PARAMS, **params}
    return pn.template.FastListTemplate(**params)
