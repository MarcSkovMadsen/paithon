import random

import panel as pn
import param

pn.extension(sizing_mode="stretch_width")


def dummy_model():
    val = float(random.randint(0, 100)) / 100
    return [
        {"label": "Egyptian cat", "score": val * 5 / 15},
        {"label": "tabby, tabby cat", "score": val * 4 / 15},
    ]


class ClassificationPlot(pn.reactive.ReactiveHTML):
    output_json = param.List()
    data = param.List(constant=True)
    _template = """<div id="component"></div>"""
    _scripts = {
        "output_json": """console.log("x")""",
    }


plot = ClassificationPlot(output_json=dummy_model())

run_button = pn.widgets.Button(name="Run Classification", button_type="primary")


def run_classification(_):
    with param.edit_constant(plot):
        plot.output_json = [dummy_model()]


run_button.on_click(run_classification)

pn.Column(run_button, plot, plot.controls(jslink=True)).servable()
