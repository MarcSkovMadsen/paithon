"""An application testing the `interactive` function"""
import time

import panel as pn

from paithon import interactive


def create_interface(inputs, outputs) -> pn.Row:
    """Returns a layouts containing the inputs and outputs"""
    if not isinstance(inputs, tuple):
        inputs = (inputs,)
    return pn.Row(pn.Column(*inputs), outputs)


def test_multi_output():
    """Demonstrates that we can make a model with two outputs interactive"""

    def model(value):
        time.sleep(0.3)
        return {"data": [value]}, f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3"

    inputs, outputs = interactive(
        model,
        inputs=[pn.widgets.Select(value=1, options=[1, 2, 3, 4])],
    )
    return create_interface(inputs, outputs)


def test_alternative_output():
    """Demonstrates that we can output to a specific pane"""

    def model(value):
        time.sleep(0.3)
        return f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3"

    select = pn.widgets.Select(value=1, options=[1, 2, 3, 4])
    inputs, outputs = interactive(
        model,
        inputs=select,
        outputs=pn.widgets.TextAreaInput,
    )
    return create_interface(inputs, outputs)


def test_fixed_num_outputs():
    """Demonstrates that we can output to a specific number of outputs"""

    def model(value):
        return list(range(1, value + 1))

    inputs, outputs = interactive(
        model, inputs=pn.widgets.IntSlider(value=0, start=0, end=5), num_outputs=5
    )
    return create_interface(inputs, outputs)


def test_generator_function_with_loading_indicator():
    """Demonstrates that we can output from a generator function and show loading indicators"""

    def model(value):
        for index in range(1, value + 1):
            time.sleep(0.2 * index)
            yield index ** 2

    inputs, outputs = interactive(
        model,
        inputs=pn.widgets.IntSlider(value=0, start=1, end=5).param.value_throttled,
        num_outputs=5,
        loading_indicator=True,
    )
    return create_interface(inputs, outputs)


if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    pn.Column(
        "# Direct to alternative output",
        test_alternative_output,
        "# Function with two outputs",
        test_multi_output(),
        "# Function with Fixed Number of Outputs",
        test_fixed_num_outputs,
        "# Generator Function with loading_indicator",
        test_generator_function_with_loading_indicator,
    ).servable()
