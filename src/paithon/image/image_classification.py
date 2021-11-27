"""A Module of tools for Image Classification"""
import random
from typing import Any, Dict, List, Tuple

import holoviews as hv
import panel as pn
import param
from PIL import Image

from ..base.classification import ClassificationPlot
from ..base.component import extract_layout_parameters
from ..base.svgs import IMAGE_CLASSIFIER_ICON
from ..shared.template import ACCENT_COLOR
from .examples import IMAGE_EXAMPLES, load_image_from_url
from .widgets.image_input import ImageInput

hv.extension("bokeh")


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


class ImageClassifier(pn.viewable.Viewer):  # pylint: disable=too-many-instance-attributes
    """A widget for classifying images.

    Inspired by the Hugging Face [ImageClassification](https://huggingface-widgets.netlify.app/)
    widget.
    """

    icon = param.String(
        IMAGE_CLASSIFIER_ICON,
        doc="""
    An image classifier icon. To be used in the header.""",
    )
    example = param.Selector(IMAGE_EXAMPLES, label="example")
    accent_color = param.Color(ACCENT_COLOR)

    model = param.Parameter()

    image = param.Parameter()

    computation_time = param.Number()
    inputs = param.Parameter()
    outputs = param.Parameter()
    output_json = param.List()

    plot = param.Parameter()
    layout_example = param.Parameter()
    layout_json = param.Parameter()
    # layout_image_input = param.ClassSelector(class_=ImageInput)
    layout_container = param.Parameter(constant=True)
    _updating = param.Boolean()

    def __init__(self, **params):
        params, layout_params = extract_layout_parameters(params)
        if "min_height" not in layout_params:
            layout_params["min_height"] = 640
        super().__init__(**params, layout_container=pn.Column(**layout_params))

        self.layout_json = pn.pane.JSON(
            depth=2,
            hover_preview=True,
            theme="light",
            name="Json Output",
            sizing_mode="stretch_width",
        )
        self.layout_image_input = ImageInput(height=300)

        @pn.depends(self.layout_image_input.param.value, watch=True)
        def _update_image_from_upload(value):
            if value:
                self._updating = True
                self.image = self.layout_image_input.get_pil_image()
                self._updating = False

        if len(IMAGE_EXAMPLES) <= 3:
            widgets = {
                "example": {
                    "type": pn.widgets.RadioButtonGroup,
                    "button_type": "success",
                    "sizing_mode": "fixed",
                }
            }
        else:
            widgets = None
        self.layout_example = pn.Param(
            self.param.example, expand_button=False, expand=False, widgets=widgets
        )[0]
        self.layout_example.name = "Example"
        self.layout_plot = ClassificationPlot(color=self.accent_color, name="Plot")
        self.layout_container[:] = [
            f"<h1>{self.icon} Image Classification</h1>",
            self.layout_example,
            self.layout_image_input,
            pn.Tabs(self.layout_plot, self.layout_json, dynamic=True),
        ]

        if self.image:
            self._updating=True
            self.param.trigger("image")
            self._updating=False

    def __panel__(self):
        return self.layout_container

    def load_image(self, url: str):
        """Loads an image from an url

        Args:
            url (str): The url to load
        """
        self.image = load_image_from_url(url)

    @param.depends("image", watch=True)
    def _update_image(self):
        if not self._updating:
            self.layout_image_input.set_value_from_pillow_image(self.image)

    @param.depends("image", watch=True)
    def _run_model(self):
        if self.model:
            self.inputs, self.outputs, self.output_json = self.model(self.image)
        else:
            self.inputs, self.outputs, self.output_json = None, None, []

    @param.depends("output_json", watch=True)
    def _update_json(self):
        self.layout_json.object = self.output_json
        self.layout_plot.output_json = self.output_json

    @param.depends("example", watch=True)
    def _update_image_from_example(self):
        self.image = self.example.image

    @pn.depends("accent_color", watch=True)
    def _handle_color_change(self):
        self.plot.color = self.accent_color
