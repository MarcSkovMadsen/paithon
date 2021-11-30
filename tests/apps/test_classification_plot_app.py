"""The ClassificationPlot plots the `object` of a classification

- It automatically determines the `theme` from the query args
- It allows you to change the color
"""
import panel as pn

from paithon.shared.pane.label import Label
from paithon.image.image_classification import dummy_model
from paithon.shared.pane.doc_string_viewer import DocStringViewer
from paithon.shared.template import ACCENT_COLOR, fastlisttemplate


def test_classification_plot():
    """Test of the ClassificationPlot"""
    _, _, output_json = dummy_model(None)
    plot = Label(
        object=output_json,
        color=ACCENT_COLOR,
        height=800,
        sizing_mode="stretch_width",
    )
    return plot


if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    classification_plot = test_classification_plot()
    run_button = pn.widgets.Button(name="Run Classification", button_type="primary")

    def _run_classification(_):
        classification_plot.object = dummy_model(None)[2]

    run_button.on_click(_run_classification)
    card = pn.layout.Card(
        DocStringViewer(object=classification_plot, height=600),
        header="# ClassificationPlot",
        collapsed=True,
    )
    fastlisttemplate(
        title="ClassificationPlot",
        sidebar=[run_button, classification_plot.controls(jslink=False)],
        main=[card, classification_plot],
    ).servable()
