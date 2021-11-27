"""The Screenshot widget allows you to take screenshot of objects or selections in your app."""
import panel as pn
import param

from ...base.component import get_theme
from ...base.reactive import read_scripts

THEME_BGCOLOR = {
    "default": "white",
    "dark": "black",
}


class Screenshot(pn.reactive.ReactiveHTML):
    """Widget for taking a screenshot of a Panel 'object' or a 'selection' in the document.
    You can specify the actions to take with the screenshot. The default is to download it."""

    object = param.Parameter(
        doc="""An object to take a screenshot of. If provided the object will
    be layout inside the Screenshot element and the `target` is set to 'object'"""
    )
    selection = param.String(
        "body",
        doc="""A selection like 'body' or '#main' to take a screenshot
    of.""",
    )
    target = param.Selector(
        default="selection",
        objects=["object", "selection"],
        doc="""
    The element to take the screenshot of. One of 'object' or 'selection'.
    """,
    )
    take = param.Event(
        label="Screenshot",
        doc="""
    If activated a screenshot is taken. Include screenshot.param.take in your app if you would like
    a 'Screenshot' button.
    """,
    )

    format = param.Selector(default="png", objects=["png", "jpeg", "svg"])
    scale = param.Number(
        1.0,
        bounds=(0.0, 1.0),
        doc="""
    A number for image scaling""",
    )
    quality = param.Number(
        1.0,
        bounds=(0.0, 1.0),
        doc="""
    A number between 0 and 1 indicating image quality (e.g. 0.92 => 92%) of the JPEG image.
    Defaults to 1.0 (100%)""",
    )
    bgcolor = param.Color("white")

    actions = param.ListSelector(
        default=["download"],
        objects=["transfer", "download", "open"],
        doc="""
    A list of actions to execute when the button is clicked. Default is 'download'. 'transfer' means
    update the uri parameter. 'open' means open screenshot in a tab in the browser.""",
    )

    download_file_name = param.String(
        "download.png",
        doc="""
    The name of the file to be downloaded""",
    )
    uri = param.String(constant=True, doc="""The screenshot downloaded as a data_uri""")
    open_target = param.Selector(
        default="_blank",
        objects=["_blank", "_self", "new"],
        doc="""
    The target tab for the 'open' action. Default is '_blank', i.e. in a new tab.""",
    )
    takes = param.Integer(label="Screenshots", doc="The number of screenshots taken")

    width = param.Integer(default=300)
    height = param.Integer(default=47)
    margin = param.Parameter(default=0)

    _template = """
<div id="container" style="height:100%;width:100%">
${object}
</div>
"""
    _child_config = {"name": "literal"}

    _scripts = read_scripts("screenshot.js", __file__)

    __javascript__ = [
        "https://cdn.jsdelivr.net/npm/dom-to-image-improved@2.8.0/src/dom-to-image-improved.min.js"
    ]

    def __init__(self, **params):
        if "object" in params and "target" not in params:
            params["target"] = "object"
        if "bgcolor" not in params:
            params["bgcolor"] = THEME_BGCOLOR[get_theme()]
        super().__init__(**params)

    @param.depends("take", watch=True)
    def _handle_click(self):
        self.takes += 1

    @param.depends("object", watch=True)
    def _handle_object_changed(self):
        if self.object:
            self.target = "object"
        else:
            self.target = "selection"

    @param.depends("selection", watch=True)
    def _handle_selection_changed(self):
        if self.selection or not self.object:
            self.target = "selection"
        else:
            self.target = "object"

    @param.depends("format", watch=True)
    def _handle_format(self):
        if "." in self.download_file_name:
            split = self.download_file_name.split(".")
            split[-1] = self.format
            self.download_file_name = ".".join(split)
