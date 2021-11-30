"""Module of classification tools"""

import panel as pn
import param

from ...base.reactive import read_scripts
from ...base.component import get_theme

ACCENT_COLOR = "#0072B5"


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


class Label(pn.reactive.ReactiveHTML):
    """The ClassificationPlot provides plots of the output of a classification, i.e. the *labels*
    and their *score*."""

    object = param.List(
        doc="""
    The output of a classification""", precedence=-1
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
    top = param.Integer(5, bounds=(1,None), doc="""
    Displays the top number of elements
    """)

    label = param.String("ORANGUTAN", constant=True)
    top_object = param.List(constant=True)

    _base_options = param.Dict(CONFIG, constant=True)
    # <div id="label" style="height:50%;font-size:50px;text-align:center;font-weight:900">${label}</div>
    _template = """
    <svg xmlns="http://www.w3.org/2000/svg" height="50%" width="100%" viewBox="0 0 110 50">
        <text x="50%" y="50%" text-anchor="middle" alignment-baseline="central" dominant-baseline="central" font-size="1em">${label}</text>
      </svg>
    <div id="component" style="height:50%;width:100%"><div id="plot"></div></div>
    """


    _scripts = read_scripts("label.js", __file__)

    __javascript__ = ["https://cdn.jsdelivr.net/npm/apexcharts"]

    def __init__(self, **params):
        params["theme"] = params.get("theme", get_theme())

        super().__init__(**params)

    @param.depends("object", watch=True)
    def _handle_change(self):
        if not self.object:
            self.label=""
            self.top_object = []
            return

        top_object = sorted(self.object, key=lambda x: -x["score"])
        if len(top_object)>self.top:
            top_object=top_object[0:self.top]
        with param.edit_constant(self):
            self.label=top_object[0]["label"].upper()
            self.top_object=top_object