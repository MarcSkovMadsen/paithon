"""The `interactive` function makes your model interactive in no time."""
from typing import Optional

import panel as pn
import param

from .pipe import pipe


def _to_widget_and_parameter(value):
    if callable(value):
        return _to_widget_and_parameter(value())
    if isinstance(value, param.Parameterized):
        return value, value.param.value
    if isinstance(value, param.Parameter):
        return value.owner, value
    raise ValueError(f"The type of input provided {value} is not supported")


def xbind(function, inputs):
    if isinstance(inputs, dict):
        inputs_and_parameters = {
            key: _to_widget_and_parameter(input) for key, input in inputs.items()
        }
        inputs = {key: value[0] for key, value in inputs_and_parameters.items()}
        parameters = {key: value[1] for key, value in inputs_and_parameters.items()}
        ifunction = pn.bind(function, **parameters)
        return ifunction, inputs
    if isinstance(inputs, (list, tuple)):
        inputs_and_parameters = tuple(_to_widget_and_parameter(input) for input in inputs)
        inputs, parameters = tuple(zip(*inputs_and_parameters))
        ifunction = pn.bind(function, *parameters)
        return ifunction, inputs

    inputs, parameter = _to_widget_and_parameter(inputs)
    ifunction = pn.bind(function, parameter)
    return ifunction, inputs


def _to_tuple(outputs) -> tuple:
    if not outputs:
        return tuple()
    if not isinstance(outputs, (list, tuple)):
        return (outputs,)
    return tuple(outputs)


def interactive(
    model, inputs, outputs=None, num_outputs: Optional[int] = None, loading_indicator=False
):
    """Returns input widgets and outputs for your model. The inputs

    Args:
        function ([type]): [description]
        inputs ([type]): [description]
        outputs ([type], optional): [description]. Defaults to None.
        num_outputs (Optional[int], optional): [description]. Defaults to None.
        loading_indicator (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    ifunction, inputs = xbind(model, inputs)

    outputs = _to_tuple(outputs)
    outputs = pipe(
        ifunction, *outputs, loading_indicator=loading_indicator, num_outputs=num_outputs
    )
    return inputs, outputs
