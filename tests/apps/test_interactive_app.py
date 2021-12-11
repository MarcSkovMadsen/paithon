"""An application testing the `interactive` function"""
import time

import panel as pn

from paithon import interactive


def test_multi_output():
    """Demonstrates that we can make a model with two outputs interactive"""

    def model(value):
        return f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3", f'<img id="slideshow" height="300" src="https://picsum.photos/800/300?image={value}"/>'

    return interactive(
        model,
        inputs=[pn.widgets.Select(value=1, options=[1, 2, 3, 4])],
    )



def test_alternative_output():
    """Demonstrates that we can output to a specific pane"""

    def model(value):
        time.sleep(0.3)
        return f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3"

    select = pn.widgets.Select(value=1, options=[1, 2, 3, 4])
    return interactive(
        model,
        inputs=select,
        outputs=pn.widgets.TextAreaInput,
    )



def test_fixed_num_outputs():
    """Demonstrates that we can output to a specific number of outputs"""

    def model(value):
        return list(range(1, value + 1))

    return interactive(
        model, inputs=pn.widgets.IntSlider(value=0, start=0, end=5), num_outputs=5
    )



def test_generator_function_with_loading_indicator():
    """Demonstrates that we can output from a generator function and show loading indicators"""

    def model(value):
        for index in range(1, value + 1):
            time.sleep(0.2 * index)
            yield index ** 2

    return interactive(
        model,
        inputs=pn.widgets.IntSlider(value=0, start=1, end=5).param.value_throttled,
        num_outputs=5,
        loading_indicator=True,
    )

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
