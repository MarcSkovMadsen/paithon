import random
from io import BytesIO
from typing import Dict, Tuple

import holoviews as hv
import panel as pn
import param
import requests
from bokeh.models import HoverTool
from PIL import Image

from .base.pillow import ImageViewer

hv.extension("bokeh")

LAYOUT_PARAMETERS = {"background", "height", "width", "sizing_mode"}

IMAGE_CLASSIFIER_ICON = """<svg xmlns="http://www.w3.org/1500/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" fill="currentColor" focusable="false" role="img" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><polygon points="4 20 4 22 8.586 22 2 28.586 3.414 30 10 23.414 10 28 12 28 12 20 4 20"></polygon><path d="M19,14a3,3,0,1,0-3-3A3,3,0,0,0,19,14Zm0-4a1,1,0,1,1-1,1A1,1,0,0,1,19,10Z"></path><path d="M26,4H6A2,2,0,0,0,4,6V16H6V6H26V21.17l-3.59-3.59a2,2,0,0,0-2.82,0L18,19.17,11.8308,13l-1.4151,1.4155L14,18l2.59,2.59a2,2,0,0,0,2.82,0L21,19l5,5v2H16v2H26a2,2,0,0,0,2-2V6A2,2,0,0,0,26,4Z"></path></svg>"""


def dummy_model(image: Image.Image):
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


def extract_layout_parameters(params: Dict) -> Tuple[Dict, Dict]:
    layout_params = {}
    non_layout_params = {}
    for key, val in params.items():
        if key in LAYOUT_PARAMETERS:
            layout_params[key] = val
        else:
            non_layout_params[key] = val
    return non_layout_params, layout_params


class ImageExample(param.Parameterized):
    url = param.String()


EXAMPLES = [
    {
        "url": "https://huggingface.co/datasets/mishig/sample_images/resolve/main/tiger.jpg",
        "name": "Tiger",
    },
    {
        "url": "https://huggingface.co/datasets/mishig/sample_images/resolve/main/teapot.jpg",
        "name": "Teapot",
    },
    {
        "url": "https://huggingface.co/datasets/mishig/sample_images/resolve/main/palace.jpg",
        "name": "Palace",
    },
]
EXAMPLES = [ImageExample(**kwargs) for kwargs in EXAMPLES]


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
    example = param.Selector(EXAMPLES, label="example")

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
        self.layout_image = ImageViewer(background="blue")
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
        self.image = Image.open(requests.get(url, stream=True, verify=False).raw)

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
        self.load_image(self.example.url)

    @pn.depends("layout_fileinput.value", watch=True)
    def _update_image_from_upload(self):
        if self.layout_fileinput.value:
            stream = BytesIO(self.layout_fileinput.value)
            self.image = Image.open(stream)  # .convert("RGBA")
