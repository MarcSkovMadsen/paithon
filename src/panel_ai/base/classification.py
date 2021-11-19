"""Module of classification tools"""

import panel as pn
import param

from ..base.reactive import read_scripts
from .component import get_theme

ACCENT_COLOR = "#A01346"


CONFIG = {
    "series": [
        {
            "name": "Score",
            "data": [
                {"x": "Egyptian cat", "y": 1},
                {"x": "tabby, tabby cat", "y": 21.0},
                {"x": "tiger cat", "y": 15.0},
                {"x": "lynx, catamount", "y": 10.0},
                {"x": "Siamese cat, Siamese", "y": 5.0},
            ],
        },
    ],
    "chart": {"type": "bar", "height": "100%"},
    "plotOptions": {
        "bar": {
            "borderRadius": 4,
            "horizontal": True,
            "dataLabels": {"position": "bottom"},
        }
    },
    "theme": {"mode": "light"},
    "colors": [ACCENT_COLOR],
    "title": {"text": "Score", "align": "center", "floating": True},
    "dataLabels": {
        "enabled": True,
        "textAnchor": "start",
    },
    "xaxis": {"type": "category", "min": 0, "max": 100, "labels": {"trim": True}},
}


class ClassificationPlot(pn.reactive.ReactiveHTML):
    """The ClassificationPlot provides plots of the output of a classification, i.e. the *labels*
    and their *score*."""

    output_json = param.List(
        doc="""
    The output of the classification"""
    )
    color = param.Color(
        ACCENT_COLOR,
        """
    The color of the bars of the plot""",
    )
    theme = param.Selector(
        default="default",
        objects=["default", "dark"],
        constant=True,
        doc="""
    The theme of the plot. Either 'default' or 'dark'""",
    )

    _base_options = param.Dict(CONFIG, constant=True)

    _template = """<div id="component" style="height:100%;width:100%"><div id="plot"></div></div>"""

    _scripts = read_scripts("classification.js", __file__)

    __javascript__ = ["https://cdn.jsdelivr.net/npm/apexcharts"]

    def __init__(self, **params):
        params["theme"] = params.get("theme", get_theme())

        super().__init__(**params)
