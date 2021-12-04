import time

import panel as pn

from paithon import interactive


def create_layout(inputs, outputs):
    if not isinstance(inputs, tuple):
        inputs = (inputs,)
    return pn.Row(pn.Column(*inputs), outputs)


def test_multi_output():
    def model(value):
        time.sleep(0.3)
        return {"data": [value]}, f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3"

    inputs, outputs = interactive(
        model,
        inputs=[pn.widgets.Select(value=1, options=[1, 2, 3, 4])],
    )
    return create_layout(inputs, outputs)


def test_alternative_output():
    def model(value):
        time.sleep(0.3)
        return f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3"

    select = pn.widgets.Select(value=1, options=[1, 2, 3, 4])
    inputs, outputs = interactive(
        model,
        inputs=select,
        outputs=pn.pane.Str,
    )
    return create_layout(inputs, outputs)

def test_fixed_num_outputs():
    def model(value):
        return [value for value in range(0,value)]
    slider = pn.widgets.IntSlider(value=0, start=1, end=10)
    inputs, outputs = interactive(model,inputs=slider, num_outputs=10)
    return create_layout(inputs, outputs)

if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    pn.Column(
        "# Test Alternative Output",
        test_alternative_output(),
        "# Test Multi Output",
        test_multi_output(),
        "# Fixed Number of Outputs",
        test_fixed_num_outputs
    ).servable()
