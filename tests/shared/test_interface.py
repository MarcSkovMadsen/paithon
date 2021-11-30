import panel as pn
import param
import pytest
from paithon import Interactive
from panel.layout.base import ListLike
from paithon.interactive import Model, InteractiveApi, InteractiveView, ModelRunner, RunStats

from paithon.shared.widgets.screenshot import Screenshot
from paithon.image.widgets import ImageInput

def pass_through(value1, value2):
    return value1 + value2

class ImageClassificationModel(Model):
    value1 = param.String("1")
    value2 = param.String("2")

    _function = staticmethod(pass_through)

@pytest.fixture
def model():
    return ImageClassificationModel

@pytest.fixture
def inputs():
    return {"value1": pn.widgets.TextAreaInput()}

@pytest.fixture
def outputs():
    return [pn.pane.Str()]

@pytest.fixture
def clean_model():
    return ImageClassificationModel.instance()


@pytest.fixture
def clean_inputs():
    return {"value1": pn.widgets.TextAreaInput(), "value2": pn.widgets.TextAreaInput()}

@pytest.fixture
def clean_outputs():
    return [pn.pane.Str()]

def test_empty_constructor():
    with pytest.raises(TypeError):
        Interactive()


def test_constructor_without_model(inputs, outputs):
    with pytest.raises(TypeError):
        Interactive(inputs=inputs, outputs=outputs)


@pytest.mark.parametrize("inputs", [
    None,
])
def test_clean_inputs(inputs, clean_model):
    # When
    inputs = Interactive._clean_inputs(inputs, clean_model)
    # Then
    assert isinstance(inputs, dict)
    assert len(inputs)==2

@pytest.mark.parametrize("outputs", [
    pn.pane.Str,
    [pn.pane.Str],
    pn.pane.Str(),
    [pn.pane.Str()],
])
def test_clean_outputs(outputs):
    # When
    outputs = Interactive._clean_outputs(outputs)
    # Then
    assert len(outputs)==1
    assert isinstance(outputs[0], pn.pane.Str)


def test_constructor_without_outputs(model, inputs):
    with pytest.raises(TypeError):
        Interactive(model=model, inputs=inputs)

def test_raised_error_if_model_not_a_callable(inputs, outputs):
    with pytest.raises(TypeError):
        Interactive(model="dummy", inputs=inputs, outputs=outputs)

def test_constructor(model, inputs, outputs):
    # When
    interactive = Interactive(model=model, inputs=inputs, outputs=outputs)

    # Then
    assert isinstance(interactive, param.Parameterized)
    assert interactive.model==model
    assert interactive.inputs==inputs
    assert interactive.outputs==outputs

    assert isinstance(interactive.view.inputs, dict)
    assert isinstance(interactive.view.outputs, list)
    assert isinstance(interactive.view.model, Model)

    assert interactive.name != ""
    assert interactive.description == ""
    assert interactive.article == ""

    assert interactive.arguments == []
    assert interactive.result == []

    assert interactive.submit is False
    assert interactive.submit_disabled is True

    assert interactive.screenshot is False
    assert interactive.screenshot_disabled is False

    assert interactive.flag is False
    assert interactive.flag_options == []
    assert interactive.flag_disabled is False

    assert isinstance(interactive.view, InteractiveView)
    assert isinstance(interactive.api, InteractiveApi)

    assert callable(interactive.api.post)


def test_constructor_with_single_input(model, inputs, outputs, clean_model, clean_inputs, clean_outputs):
    # When
    interactive = Interactive(model=model, inputs=inputs, outputs=outputs)
    view = interactive.view
    # Then
    assert view.model.value1 == clean_model.value1
    assert view.model.value2 == clean_model.value2
    assert set(view.inputs.keys()) == set(clean_inputs.keys())
    assert [type(item) for item in view.outputs]==[type(item) for item in clean_outputs]


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

def test_model_runner(clean_model):
    # Given
    stats = RunStats()
    # When
    stats.update(duration=1.2)
    # Asserts
    assert stats.runs==1
    assert stats.duration_total==1.2
    assert stats.duration_avg==1.2
    # When
    stats.update(duration=2.4)
    # Asserts
    assert stats.runs==2
    assert stats.duration_total==pytest.approx(3.6)
    assert stats.duration_avg==pytest.approx(1.8)

def test_model_runner(clean_model):
    # When
    runner = ModelRunner(value=clean_model)
    # Then
    assert runner.value==clean_model
    assert isinstance(runner.stats, RunStats)
    assert runner.stats.runs==0
    # When
    result = runner.run()
    # Then
    assert runner.result==result
    assert runner.kwargs
    assert runner.stats.runs==1



def test_app():
    interactive = Interactive(
        model=ImageClassificationModel,
        outputs=[pn.pane.Str]
    )
    return interactive

if __name__.startswith("bokeh"):
    pn.extension(sizing_mode="stretch_width")
    test_app().view.servable()