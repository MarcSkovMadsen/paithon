import param
import panel as pn

def _to_widget_and_parameter(value):
    if callable(value):
        return _to_widget_and_parameter(value())
    if isinstance(value, param.Parameterized):
        return value, value.param.value
    if isinstance(value, param.Parameter):
        return value.owner, value
    raise ValueError(f"The type of input provided {value} is not supported")


def pipe_from(function, inputs):
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
        return ifunction, pn.Column(*inputs)

    inputs, parameter = _to_widget_and_parameter(inputs)
    ifunction = pn.bind(function, parameter)
    return ifunction, inputs
