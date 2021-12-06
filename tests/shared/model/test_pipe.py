import panel as pn
import param
import pytest

from paithon import pipe_to
from paithon.interactive.pipe_to_pipes import NONE_OR_EMPTY_HACK
from paithon.interactive.pipe_to import (
    _adjust_results,
    _create_pipes,
    _get_pipe,
    _set_results,
    _validate_function,
)


def single_factor_model(value):
    return value


def two_factor_model(value1, value2):
    return value1, value2


@pytest.fixture
def widget1():
    return pn.widgets.TextInput()


@pytest.fixture
def isingle_factor_model(widget1):
    return pn.bind(single_factor_model, widget1)


@pytest.fixture
def widget2():
    return pn.widgets.TextInput()


@pytest.fixture
def itwo_factor_model(widget1, widget2):
    return pn.bind(two_factor_model, widget1, widget2)


class parameterized_model(param.Parameterized):
    pass


class CustomObjectOutput(param.Parameterized):
    object = param.Parameter()


class CustomValueOutput(param.Parameterized):
    value = param.Parameter()


def test_invalid_inputs():
    with pytest.raises(ValueError):
        _validate_function(two_factor_model)


def test_constructor():
    input1 = pn.widgets.TextInput()
    input2 = pn.widgets.TextInput()

    imodel = pn.bind(two_factor_model, value1=input1, value2=input2)
    # When
    output1, output2 = pipe_to(imodel, pn.pane.Str, pn.pane.Str)
    # Then
    assert isinstance(output1, pn.pane.Str)
    assert isinstance(output2, pn.pane.Str)

    # When
    input1.value = "Hello"
    assert output1.object == input1.value
    input2.value = "World"
    assert output2.object == input2.value


def test_pipe_can_replace_pn_panel():
    # Given
    def model(value1):
        return value1

    input1 = pn.widgets.TextInput()

    imodel = pn.bind(model, value1=input1)
    # When
    output1 = pipe_to(imodel)
    # Then
    assert isinstance(output1, pn.param.ParamMethod)
    assert isinstance(output1._pane, pn.pane.Markdown)

    # When
    input1.value = "abcd"
    assert isinstance(output1._pane, pn.pane.Markdown)
    assert output1._pane.object == input1.value


def test_pipe_can_infer_outputs():
    # Given
    def model(value1, value2):
        return value1, value2

    input1 = pn.widgets.TextInput()
    input2 = pn.widgets.TextInput()

    imodel = pn.bind(model, value1=input1, value2=input2)
    # When
    output1, output2 = pipe_to(imodel)
    # Then
    assert isinstance(output1, pn.param.ParamMethod)
    assert isinstance(output2, pn.param.ParamMethod)

    # When
    input1.value = "Hello"
    assert output1._pane.object == input1.value
    input2.value = "World"
    assert output2._pane.object == input2.value


def test_pipe_constructor_can_infer():
    pipes = _create_pipes(("a",), tuple())
    assert len(pipes) == 1
    pipe_ = pipes[0]
    assert pipe_.object == "a"
    assert isinstance(pipe_.output, pn.param.ParamMethod)
    assert isinstance(pipe_.output._pane, pn.pane.Markdown)
    assert pipe_.output._pane.object == pipe_.object
    # When
    new = {"data": "value"}
    pipe_.object = new
    assert isinstance(pipe_.output._pane, pn.pane.JSON)
    assert pipe_.output._pane.object == pipe_.object


def test_pipe_multi_output_constructor(itwo_factor_model):
    outputs = pipe_to(itwo_factor_model, pn.pane.Str, pn.pane.Str)
    assert isinstance(outputs, pn.Column)
    outputs = pipe_to(itwo_factor_model, pn.pane.Str, pn.pane.Str, default_layout=pn.Row)
    assert isinstance(outputs, pn.Row)


@pytest.mark.parametrize(
    ["results", "num_results", "adjusted"],
    [
        ((1,), None, (1,)),
        ((1,), 0, ()),
        ((1,), 1, (1,)),
        ((1,), 2, (1, None)),
        ((1,), 3, (1, None, None)),
        ((1, 2, 3), 2, (1, 2)),
        ((1, 2, 3), 1, (1,)),
        ((1, 2, 3), 0, ()),
        ("a", None, ("a",)),
        ("a", 1, ("a",)),
        ("a", 2, ("a", None)),
    ],
)
def test_adjust_results(results, num_results, adjusted):
    assert tuple(_adjust_results(results=results, num_results=num_results)) == adjusted


def test_pipe_to_extra_outputs():
    slider = pn.widgets.FloatSlider(value=0, start=1, end=10)

    def model(value):
        output = [value for value in range(0, value)]
        return output

    imodel = pn.bind(model, slider)
    outputs = pipe_to(imodel, num_outputs=10)

    assert len(outputs) == 10
    assert all(tuple(output._pane.object == NONE_OR_EMPTY_HACK for output in outputs))

    slider.value = 10
    assert all(tuple(output._pane.object == index for index, output in enumerate(outputs)))

    slider.value = 9
    assert all(tuple(output._pane.object == index for index, output in enumerate(outputs[0:9])))
    assert outputs[9]._pane.object is NONE_OR_EMPTY_HACK


def test_set_results_works_with_generator():
    """Being able to set results from a generator is important to enable gradually updating the
    outputs as the results become available."""
    results_generator = (index for index in range(0, 3))
    pipes = tuple(_get_pipe(output=lambda x: str(x), object=-1) for index in range(0, 4))
    _set_results(results_generator, *pipes)
    assert not pipes[3].object
