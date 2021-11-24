"""An application for manually testing the ImageInput"""
import panel as pn

from paithon.image.examples import IMAGE_EXAMPLES
from paithon.image.widgets.image_input import ImageInput
from paithon.shared.pane.doc_string_viewer import DocStringViewer
from paithon.shared.param import SortedParam
from paithon.shared.template import fastlisttemplate


def test_app() -> ImageInput:
    """Returns an example ImageInput app for testing purposes."""
    data_uri = IMAGE_EXAMPLES[0].data_uri
    image_input = ImageInput(width=200, height=200, min_height=600, sizing_mode="stretch_both")
    image_input.set_value_from_data_uri(data_uri)
    return image_input


if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    app = test_app()
    card = pn.layout.Card(
        DocStringViewer(object=app, height=600),
        header="# ImageInput",
        collapsed=True,
    )

    def _get_url(value):
        if value:
            return "_url: " + value[0:50] + "..."
        return "No Image Loaded"

    iurl = pn.bind(_get_url, value=app.param.uri)

    progress = pn.widgets.Progress(value=-1, name="Progess", sizing_mode="stretch_width")

    @pn.depends(app.param.progress, watch=True)
    def _update_progress(value):
        progress.value = value

    reset = pn.widgets.Button()
    controls = SortedParam(
        app,
        parameters=[
            "accept",
            "filename",
            "mime_type",
            "fit",
            "max_size_in_mega_bytes",
            "progress",
            "height",
            "width",
            "sizing_mode",
            "visible",
            "loading",
        ],
        widgets={
            "accept": {"height": 120},
            "height": {"start": 0, "end": 2000},
            "max_size_in_mega_bytes": {"start": 1, "end": 15},
            "width": {"start": 0, "end": 3000},
        },
    )

    fastlisttemplate(
        title="ImageInput",
        sidebar=[controls],
        main=[
            card,
            pn.Column(app, sizing_mode="stretch_both", margin=0),
            pn.Column("### Change", progress, pn.panel(iurl, height=50)),
        ],
    ).servable()
