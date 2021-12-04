import panel as pn
import param
import pytest

from paithon import pipe
from paithon.model.pipe import _adjust_results, _create_pipes, _validate_function


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
    output1, output2 = pipe(imodel, pn.pane.Str, pn.pane.Str)
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
    output1 = pipe(imodel)
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
    output1, output2 = pipe(imodel)
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
    outputs = pipe(itwo_factor_model, pn.pane.Str, pn.pane.Str)
    assert isinstance(outputs, pn.Column)
    outputs = pipe(itwo_factor_model, pn.pane.Str, pn.pane.Str, default_layout=pn.Row)
    assert isinstance(outputs, pn.Row)


def test_adjust_results():
    assert _adjust_results(None, None) == tuple()
    assert _adjust_results((1,), None) == (1,)
    assert _adjust_results((1,), 0) == tuple()
    assert _adjust_results(None, 1) == (None,)
    assert _adjust_results(None, 2) == (None, None)
    assert _adjust_results((1,), 1) == (1,)
    assert _adjust_results((1,), 2) == (1, None)
    assert _adjust_results((1,), 3) == (1, None, None)
    assert _adjust_results((1, 2, 3), 2) == (1, 2)
    assert _adjust_results((1, 2, 3), 1) == (1,)
    assert _adjust_results((1, 2, 3), 0) == tuple()
    assert _adjust_results("a", None) == ("a")
    assert _adjust_results("a", 1) == ("a")
    assert _adjust_results("a", 2) == ("a", None)

def test_pipe_to_extra_outputs():
    slider = pn.widgets.FloatSlider(value=0, start=1, end=10)
    def model(value):
        return [value for value in range(0,value)]
    imodel=pn.bind(model, slider)
    outputs=pipe(imodel, num_outputs=10)

    assert len(outputs)==10
    assert all(tuple(output._pane.object==None for output in outputs))

    slider.value=10
    assert all(tuple(output._pane.object==index for index, output in enumerate(outputs)))

    slider.value=9
    assert all(tuple(output._pane.object==index for index, output in enumerate(outputs[0:9])))
    assert outputs[9]._pane.object is None