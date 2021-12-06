import panel as pn
import param
import pytest

from paithon import interactive
from paithon.model.interactive import _to_widget_and_parameter, xbind


def test_interactive():
    # Given
    def model(value1, value2):
        return value1, value2

    input1_org = pn.widgets.TextInput
    input2_org = pn.widgets.TextInput()
    output1_org = pn.pane.Str
    output2_org = pn.pane.Str(name="Output 2")
    # When
    inputs, outputs = interactive(
        model, inputs=[input1_org, input2_org], outputs=[output1_org, output2_org]
    )
    # Then
    input1, input2 = inputs
    assert isinstance(input1, pn.widgets.TextInput)
    assert input2 == input2_org

    output1, output2 = outputs
    assert isinstance(output1, pn.pane.Str)
    assert output2 == output2_org

    input1.value = "Hello"
    output1.object == input1.value

    input2.value = "World"
    output2.object == input1.value


def test_multi_output():
    def model(value):
        return {"data": [value]}, f"https://audio.qurancdn.com/wbw/001_001_00{value}.mp3"

    inputs, outputs = interactive(
        model,
        inputs=[pn.widgets.Select(value=1, options=[1, 2, 3, 4])],
    )
    assert outputs[0].object
    assert outputs[1].object
    return pn.Row(pn.Column(*inputs), outputs)


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
    return pn.Row(pn.Column(inputs), outputs)


@pytest.mark.parametrize("input", [pn.widgets.IntSlider, pn.widgets.IntSlider()])
def test_to_widget_and_parameter(input):
    widget, parameter = _to_widget_and_parameter(input)

    assert isinstance(widget, pn.widgets.IntSlider)
    assert isinstance(parameter, param.Integer)
    assert parameter.name == "value"
    assert parameter.owner is widget


def test_to_widget_and_parameter():
    input = pn.widgets.IntSlider().param.value_throttled
    widget, parameter = _to_widget_and_parameter(input)

    assert isinstance(widget, pn.widgets.IntSlider)
    assert isinstance(parameter, param.Integer)
    assert parameter.name == "value_throttled"
    assert parameter.owner is widget


def test_to_ifunction_and_inputs_single_slider():
    # Given
    slider = pn.widgets.IntSlider()

    def function(x):
        return x

    # When
    ifunction, inputs = xbind(function, slider)
    # Then
    assert inputs is slider
    assert "__wrapped__" in ifunction.__dict__
    assert ifunction.__dict__["_dinfo"]["kw"]["__arg0"] is slider.param["value"]


def test_to_ifunction_and_inputs_single_value_throttled_of_slider():
    # Given
    slider = pn.widgets.IntSlider()

    def function(x):
        return x

    # When
    ifunction, inputs = xbind(function, slider.param.value_throttled)
    # Then
    assert inputs is slider
    assert "__wrapped__" in ifunction.__dict__
    assert ifunction.__dict__["_dinfo"]["kw"]["__arg0"] is slider.param["value_throttled"]


def test_to_ifunction_and_inputs_multi_args():
    # Given
    slider1 = pn.widgets.IntSlider()
    slider2 = pn.widgets.IntSlider()

    def function(x, y):
        return x + y

    # When
    ifunction, inputs = xbind(function, [slider1, slider2.param.value_throttled])
    # Then
    assert inputs[0] is slider1
    assert inputs[1] is slider2
    assert "__wrapped__" in ifunction.__dict__
    assert ifunction.__dict__["_dinfo"]["kw"]["__arg0"] is slider1.param["value"]
    assert ifunction.__dict__["_dinfo"]["kw"]["__arg1"] is slider2.param["value_throttled"]


def test_to_ifunction_and_inputs_multi_kwargs():
    # Given
    slider1 = pn.widgets.IntSlider()
    slider2 = pn.widgets.IntSlider()

    def function(x, y):
        return x + y

    # When
    ifunction, inputs = xbind(function, {"x": slider1, "y": slider2.param.value_throttled})
    # Then
    assert inputs["x"] is slider1
    assert inputs["y"] is slider2
    assert "__wrapped__" in ifunction.__dict__
    assert ifunction.__dict__["_dinfo"]["kw"]["x"] is slider1.param["value"]
    assert ifunction.__dict__["_dinfo"]["kw"]["y"] is slider2.param["value_throttled"]
