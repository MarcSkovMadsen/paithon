import pytest

from paithon.model.runner import ModelRunner, ModelStats

def test_model_runner(model_runner, clean_model):
    # Then
    assert model_runner.value==clean_model
    assert model_runner.auto_submit
    assert isinstance(model_runner.stats, ModelStats)
    assert model_runner.stats.runs==0
def test_can_run(model, model_runner):
    # When
    result = model_runner.run(value1="11", value2="22")
    # Then
    assert result==model(value1="11", value2="22")
    assert model_runner.result==result
    assert model_runner.kwargs
    assert model_runner.stats.runs==1

def test_can_submit(model, model_runner):
    # When
    model_runner.submit=True
    # Then
    assert model_runner.submit==False
    assert model_runner.result==model()
    assert model_runner.stats.runs==1

def test_with_autosubmit(model, clean_model, model_runner):
    # Given
    model_runner.auto_submit=True
    # When
    clean_model.value1="11"
    # Then
    assert model_runner.result==model(value1="11")