"""An application for manually testing the docstring viewer."""
import panel as pn

from paithon.base.template import fastlisttemplate
from paithon.shared.pane.doc_string_viewer import DocStringViewer


def test_app() -> DocStringViewer:
    """Returns a DocStringViewer for manual testing.

    Returns:
        DocStringViewer: [description]
    """
    some_parameterized = DocStringViewer()
    return DocStringViewer(
        some_parameterized, sizing_mode="stretch_width", palette="Tomorrow", scroll=False
    )


if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    app = test_app()
    pn.state.location.sync(app, {"palette": "palette"})
    controls = pn.Column(
        pn.pane.Markdown("**Palette**", margin=0),
        pn.widgets.RadioBoxGroup.from_param(app.param.palette),
    )
    fastlisttemplate(
        title="DocStringViewer",
        sidebar=[controls],
        main=[app],
    ).servable()
