import panel as pn
import param
import pytest
from conftest import ImageClassificationModel

from paithon import Interface
from paithon.model.interface import InterfaceView, Model, ModelApi


def test_empty_constructor():
    with pytest.raises(TypeError):
        Interface()


def test_constructor_without_model(inputs, outputs):
    with pytest.raises(TypeError):
        Interface(inputs=inputs, outputs=outputs)


@pytest.mark.parametrize(
    "inputs",
    [
        None,
    ],
)
def test_clean_inputs(inputs, clean_model):
    # When
    inputs = Interface._clean_inputs(inputs, clean_model)
    # Then
    assert isinstance(inputs, dict)
    assert len(inputs) == 2


@pytest.mark.parametrize(
    "outputs",
    [
        pn.pane.Str,
        [pn.pane.Str],
        pn.pane.Str(),
        [pn.pane.Str()],
    ],
)
def test_clean_outputs(outputs):
    # When
    outputs = Interface._clean_outputs(outputs)
    # Then
    assert len(outputs) == 1
    assert isinstance(outputs[0], pn.pane.Str)


def test_constructor_without_outputs(model, inputs):
    with pytest.raises(TypeError):
        Interface(model=model, inputs=inputs)


def test_raised_error_if_model_not_a_callable(inputs, outputs):
    with pytest.raises(TypeError):
        Interface(model="dummy", inputs=inputs, outputs=outputs)


def test_constructor(model, inputs, outputs):
    # When
    interactive = Interface(model=model, inputs=inputs, outputs=outputs)

    # Then
    assert isinstance(interactive, param.Parameterized)
    assert interactive.model == model
    assert interactive.inputs == inputs
    assert interactive.outputs == outputs

    assert isinstance(interactive.view.inputs, dict)
    assert isinstance(interactive.view.outputs, list)
    assert isinstance(interactive.view.model, Model)

    assert interactive.name != ""
    assert interactive.description == ""
    assert interactive.article == ""

    assert interactive.arguments == []
    assert interactive.result == []

    assert interactive.submit is False

    assert interactive.screenshot is False
    assert interactive.screenshot_disabled is False

    assert interactive.flag is False
    assert interactive.flag_options == []
    assert interactive.flag_disabled is False

    assert isinstance(interactive.view, InterfaceView)
    assert isinstance(interactive.api, ModelApi)

    assert callable(interactive.api.post)


def test_constructor_with_single_input(
    model, inputs, outputs, clean_model, clean_inputs, clean_outputs
):
    # When
    interactive = Interface(model=model, inputs=inputs, outputs=outputs)
    view = interactive.view
    # Then
    assert view.model.value1 == clean_model.value1
    assert view.model.value2 == clean_model.value2
    assert set(view.inputs.keys()) == set(clean_inputs.keys())
    assert [type(item) for item in view.outputs] == [type(item) for item in clean_outputs]


@pytest.mark.parametrize(
    ["args", "kwargs", "expected"],
    [
        ((), {}, "12"),
        ((), {"value1": "a", "value2": "b"}, "ab"),
        ((), {"value1": "a"}, "a2"),
        ((), {"value2": "b"}, "1b"),
        (("c"), {}, "c2"),
        (("c", "d"), {}, "cd"),
    ],
)
def test_model(args, kwargs, expected):
    assert ImageClassificationModel(*args, **kwargs) == expected


# def test_submit(model, inputs, outputs):
#     # given
#     interactive = Interactive(model, inputs, outputs)


def test_app():
    interactive = Interface(
        model=ImageClassificationModel, outputs=[pn.pane.Str], auto_submit=False, initial_run=True
    )
    return interactive


if __name__.startswith("bokeh"):
    import logging

    logging.basicConfig(level=logging.DEBUG)
    pn.extension(sizing_mode="stretch_width")
    test_app().view.servable()
