"""Test of the ImageClassifier

"""
import panel as pn

from panel_ai.base.template import fastlisttemplate
from panel_ai.image.image_classification import ImageClassifier, dummy_model


def test_app():
    """Test of the ImageClassifier"""
    classifier = ImageClassifier(model=dummy_model, sizing_mode="stretch_width")
    classifier.load_image(url="http://images.cocodataset.org/val2017/000000039769.jpg")
    return pn.Row(classifier)


if __name__.startswith("bokeh"):
    fastlisttemplate(
        title="ImageClassifier",
        main=[__doc__, test_app()],
    ).servable()
