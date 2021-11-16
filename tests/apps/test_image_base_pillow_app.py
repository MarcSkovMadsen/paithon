"""Test of the Pillow ImageViewer

Verify

- An Image is shown
- The image is centered
- The image Height is 100%
"""
import panel as pn

from panel_ai.base.template import fastlisttemplate
from panel_ai.image.base.pillow import ImageViewer
from tests.image.conftest import get_image


def test_app():
    """Test of the Pillow ImageViewer"""
    viewer = ImageViewer(get_image())
    return pn.Row(viewer, viewer.controls())


if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    fastlisttemplate(
        title="Pillow ImageViewer",
        main=[__doc__, test_app()],
    ).servable()
