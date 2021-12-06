import panel as pn
import param
import pytest

from paithon.interactive.pipe_to_pipes import PanelPipe, ParameterizedPipe, create_pipe


@pytest.mark.parametrize("output", [pn.pane.Str, pn.pane.Str()])
def test_pipe_to_pane(output):
    # Given
    object = "hello"

    # When
    result = create_pipe(output=output, object=object)

    assert isinstance(result, ParameterizedPipe)
    assert result.parameter == "object"
    assert result.object == object
    assert isinstance(result.output, pn.pane.Str)
    assert result.output.object == result.object

    # When
    result.object = "world"
    assert result.output.object == result.object

    # When
    result.loading = True
    assert result.output.loading == result.loading
    # Then
    result.loading = False
    assert result.output.loading == result.loading


@pytest.mark.parametrize("output", [pn.widgets.TextInput, pn.widgets.TextInput()])
def test_pipe_to_widget(output):
    # Given
    object = "hello"

    # When
    result = create_pipe(output=output, object=object)

    assert isinstance(result, ParameterizedPipe)
    assert result.parameter == "value"
    assert result.object == object
    assert isinstance(result.output, pn.widgets.TextInput)
    assert result.output.value == result.object

    # When
    result.object = "world"
    assert result.output.value == result.object

    # When
    result.loading = True
    assert result.output.loading == result.loading
    # Then
    result.loading = False
    assert result.output.loading == result.loading


class CustomParameter(param.Parameterized):
    custom_value = param.String()


@pytest.mark.parametrize(
    "output", [CustomParameter.param.custom_value, CustomParameter().param.custom_value]
)
def test_pipe_to_parameter(output):
    # Given
    object = "hello"

    # When
    result = create_pipe(output=output, object=object)

    assert isinstance(result, ParameterizedPipe)
    assert result.parameter == "custom_value"
    assert result.object == object
    assert isinstance(result.output, CustomParameter)
    assert result.output.custom_value == result.object

    # When
    result.object = "world"
    assert result.output.custom_value == result.object

    # When
    result.loading = True
    assert result.output.loading == result.loading
    # Then
    result.loading = False
    assert result.output.loading == result.loading


def test_pipe_no_output():
    # Given
    output = None
    object = "hello"
    # When
    result = create_pipe(output=output, object=object)

    assert isinstance(result, PanelPipe)
    assert result.object == object
    assert isinstance(result.output, pn.param.ParamMethod)
    assert isinstance(result.output._pane, pn.pane.Markdown)
    assert result.output._pane.object == result.object

    # When
    result.object = "world"
    assert result.output._pane.object == result.object

    # When
    result.loading = True
    assert result.output._pane.loading == result.loading
    # Then
    result.loading = False
    assert result.output._pane.loading == result.loading


def test_pipe_to_function():
    # Given
    output = lambda x: x + " world"
    object = "hello"
    # When
    result = create_pipe(output=output, object=object)

    assert isinstance(result, PanelPipe)
    assert result.object == object
    assert isinstance(result.output, pn.param.ParamMethod)
    assert isinstance(result.output._pane, pn.pane.Markdown)
    assert result.output._pane.object == result.object + " world"

    # When
    result.object = "world"
    assert result.output._pane.object == result.object + " world"

    # When
    result.loading = True
    assert result.output._pane.loading == result.loading
    # Then
    result.loading = False
    assert result.output._pane.loading == result.loading
