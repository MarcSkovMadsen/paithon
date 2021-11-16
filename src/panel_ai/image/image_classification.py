"""A Module of tools for Image Classification"""
import random
from io import BytesIO
from typing import Any, Dict, List, Tuple

import holoviews as hv
import panel as pn
import param
import requests
from bokeh.models import HoverTool
from PIL import Image

from ..base.svgs import IMAGE_CLASSIFIER_ICON
from .base.pillow import ImageViewer, IMAGE_EXAMPLES, load_image_from_url

hv.extension("bokeh")

LAYOUT_PARAMETERS = {"background", "height", "width", "sizing_mode"}




# pylint: disable=unused-argument
def dummy_model(image: Image.Image) -> Tuple[Any, Any, List[Dict]]:
    """Returns a the inputs, outputs, output_json of an Image classification

    Args:
        image (Image.Image): The image to classify

    Returns:
        Tuple[Any, Any, List[Dict]]: the inputs, outputs, output_json
    """
    val = float(random.randint(0, 100)) / 100
    return (
        None,
        None,
        [
            {"label": "Egyptian cat", "score": val * 5 / 15},
            {"label": "tabby, tabby cat", "score": val * 4 / 15},
            {"label": "tiger cat", "score": val * 3 / 15},
            {"label": "lynx, catamount", "score": val * 2 / 15},
            {"label": "Siamese cat, Siamese", "score": val * 1 / 15},
        ],
    )
# pylint: enable=unused-argument

def extract_layout_parameters(params: Dict) -> Tuple[Dict, Dict]:
    layout_params = {}
    non_layout_params = {}
    for key, val in params.items():
        if key in LAYOUT_PARAMETERS:
            layout_params[key] = val
        else:
            non_layout_params[key] = val
    return non_layout_params, layout_params

def to_plot(output_json, height=200, color="red", bgcolor=None):
    if not output_json:
        return None
    output_json = sorted(output_json, key=lambda x: x["score"])
    data = output_json
    plot = hv.Bars(data, hv.Dimension("label"), "score")

    hover = HoverTool(tooltips=[("Score", "@score{0.00}")])

    plot.opts(
        responsive=True,
        height=height,
        color=color,
        bgcolor=bgcolor,
        invert_axes=True,
        ylim=(0.0, 1.0),
        default_tools=["save", hover],
    )
    # position = round(data[-1]["score"],2)
    data_labels = [
        {"label": item["label"], "position": item["score"], "score": round(item["score"], 2)}
        for item in data
    ]
    labels = hv.Labels(data=data_labels, kdims=["label", "position"], vdims="score")
    labels.opts(default_tools=["save"], labelled=[])
    return plot * labels


class ImageClassifier(pn.viewable.Viewer):
    """A widget for classifying images


    Inspired by the Hugging Face [ImageClassification](https://huggingface-widgets.netlify.app/)
    widget
    """

    icon = param.String(IMAGE_CLASSIFIER_ICON)
    example = param.Selector(IMAGE_EXAMPLES, label="example")

    model = param.Parameter()

    image = param.Parameter()

    computation_time = param.Number()
    inputs = param.Parameter()
    outputs = param.Parameter()
    output_json = param.List()

    plot = param.Parameter()
    layout_example = param.Parameter()
    layout_fileinput = param.Parameter()
    layout_json = param.Parameter()
    layout_image = param.Parameter()
    layout_container = param.Parameter(constant=True)

    def __init__(self, **params):
        params, layout_params = extract_layout_parameters(params)
        super().__init__(**params, layout_container=pn.Column(**layout_params))

        self.layout_json = pn.pane.JSON(
            depth=2,
            hover_preview=True,
            theme="light",
            name="Json Output",
            sizing_mode="stretch_width",
        )
        self.layout_fileinput = pn.widgets.FileInput(
            accept=".png,.jpg", css_classes=["file-upload"]
        )
        self.layout_example = pn.Param(self.param.example, expand_button=False, expand=True)[0]
        self.layout_example.name = "Example"
        self.layout_image = ImageViewer()
        self.layout_plot = pn.bind(to_plot, output_json=self.param.output_json)
        self.layout_container[:] = [
            f"<h1>{self.icon} Image Classification</h1>",
            self.layout_example,
            self.layout_fileinput,
            self.layout_image,
            self.layout_plot,
            self.layout_json,
        ]

    def __panel__(self):
        return self.layout_container

    def load_image(self, url):
        self.image = load_image_from_url(url)

    @param.depends("image", watch=True)
    def _update_image(self):
        self.layout_image.image = self.image

    @param.depends("image", watch=True)
    def _run_model(self):
        self.inputs, self.outputs, self.output_json = self.model(self.image)

    @param.depends("output_json", watch=True)
    def _update_json(self):
        self.layout_json.object = self.output_json
        self.plot = to_plot(self.output_json)

    @param.depends("example", watch=True)
    def _update_image_from_example(self):
        self.image = self.example.image

    @pn.depends("layout_fileinput.value", watch=True)
    def _update_image_from_upload(self):
        if self.layout_fileinput.value:
            stream = BytesIO(self.layout_fileinput.value)
            self.image = Image.open(stream)  # .convert("RGBA")
