"""Test of the Pillow ImageViewer

Verify

- An Image is shown
- The image is centered
- The image Height is 100%
"""
import panel as pn

from paithon.base.template import fastlisttemplate
from paithon.image.base.pillow import ImageViewer, IMAGE_EXAMPLES

IMAGE=IMAGE_EXAMPLES[0].image

def test_app():
    """Test of the Pillow ImageViewer"""
    viewer = ImageViewer(IMAGE)
    return pn.Row(viewer, viewer.controls())


if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    fastlisttemplate(
        title="Pillow ImageViewer",
        main=[__doc__, test_app()],
    ).servable()
