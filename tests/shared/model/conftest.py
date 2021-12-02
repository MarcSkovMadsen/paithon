"""Module of fixtures for testing Interface Functionality"""
import panel as pn
import param
import pytest
from paithon.model.interface import Model, ModelRunner


def pass_through(value1, value2):
    """Simple model function for testing"""
    return value1 + value2


class ImageClassificationModel(Model):
    """Simple Model for testing"""

    value1 = param.String("1")
    value2 = param.String("2")

    _function = staticmethod(pass_through)


@pytest.fixture
def model():
    """A value that can be provided as a model to Interface"""
    return ImageClassificationModel


@pytest.fixture
def inputs():
    """A value that can be provided as a inputs to Interface"""
    return {"value1": pn.widgets.TextAreaInput()}


@pytest.fixture
def outputs():
    """A value that can be provided as a outputs to Interface"""
    return [pn.pane.Str()]


@pytest.fixture
def clean_model():
    """The expected clean model from model"""
    return ImageClassificationModel.instance()


@pytest.fixture
def clean_inputs():
    """The expected clean inputs from model and inputs"""
    return {"value1": pn.widgets.TextAreaInput(), "value2": pn.widgets.TextAreaInput()}


@pytest.fixture
def clean_outputs():
    """The expected clean outputs from outputs"""
    return [pn.pane.Str()]

@pytest.fixture
def model_runner(clean_model):
    """The expected modelrunner from clean_model"""
    return  ModelRunner(value=clean_model)
