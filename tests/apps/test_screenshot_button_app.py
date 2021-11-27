"""An application for manually testing the Screenshot widget"""
import numpy as np
import panel as pn
from paithon.shared.template import fastlisttemplate
from paithon.shared.widgets import Screenshot, screenshot

pn.extension(sizing_mode="stretch_width")


def test_app():
    """Screenshot App for automated and manual testing"""
    _day = pn.widgets.IntSlider(value=1, start=1, end=7, name="Day", sizing_mode="fixed")
    header = pn.pane.Markdown()
    plot = pn.indicators.Trend(title="Price", height=200, sizing_mode="stretch_width")

    @pn.depends(_day, watch=True)
    def _update_zoom(value=_day.value):
        data = {"x": np.arange(24), "y": np.random.randn(24).cumsum()}
        plot.data = data
        header.object = f"# Daily Report: {value}"

    _update_zoom()
    component = pn.Column(header, plot)
    _screenshot = Screenshot(
        name="Screenshot", height=400, object=component, actions=["open"], open_target="new"
    )
    _controls = _screenshot.controls(jslink=False)
    return _controls, _screenshot, _day


if __name__.startswith("bokeh"):
    controls, screenshot, day = test_app()
    fastlisttemplate(
        title="Screenshot",
        sidebar=[controls],
        main=[
            day,
            screenshot,
            pn.widgets.Button.from_param(screenshot.param.take, button_type="primary"),
        ],
    ).servable()
