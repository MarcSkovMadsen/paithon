"""Test of the ImageClassifier

"""
import panel as pn

from panel_ai.base.template import fastlisttemplate
from panel_ai.image.image_classification import IMAGE_EXAMPLES, ImageClassifier, dummy_model
from panel_ai.shared.pane.doc_string_viewer import DocStringViewer


def test_app():
    """Test of the ImageClassifier"""
    classifier = ImageClassifier(
        image=IMAGE_EXAMPLES[0].image,
        model=dummy_model,
        name="Example",
        sizing_mode="stretch_width",
    )
    return classifier


if __name__.startswith("bokeh"):
    app = test_app()
    docs = DocStringViewer(object=app, sizing_mode="stretch_both", name="Docs")

    fastlisttemplate(
        title="ImageClassifier",
        main=[pn.Tabs(app, docs)],
    ).servable()
