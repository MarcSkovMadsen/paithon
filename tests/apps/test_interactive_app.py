import panel as pn

from paithon import interactive


def test_multi_output():
    def model(value):
        return {"data": [value]}, f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3"

    inputs, outputs = interactive(
        model,
        inputs=[pn.widgets.Select(value=1, options=[1, 2, 3, 4])],
    )
    assert outputs[0].object
    assert outputs[1].object
    return pn.Row(pn.Column(*inputs), pn.Column(*outputs))


def test_alternative_output():
    def model(value):
        return f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3"

    select = pn.widgets.Select(value=1, options=[1, 2, 3, 4])
    inputs, outputs = interactive(
        model,
        inputs=select,
        outputs=pn.pane.Str,
    )
    assert inputs == select
    assert outputs[0].object
    assert outputs[0].object
    return pn.Row(pn.Column(inputs), pn.Column(outputs))


if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    pn.Column(
        "# Test Alternative Output",
        test_alternative_output(),
        "# Test Multi Output",
        test_multi_output(),
    ).servable()
