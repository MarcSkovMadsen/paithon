import panel as pn

from .pipe import pipe


def _clean_input(input):
    if callable(input):
        return input()
    return input


def interactive(function, inputs, outputs=None):
    if isinstance(inputs, dict):
        inputs = {key: _clean_input(input) for key, input in inputs.items()}
        ifunction = pn.bind(function, **inputs)
    elif isinstance(inputs, (list, tuple)):
        inputs = tuple(_clean_input(input) for input in inputs)
        ifunction = pn.bind(function, *inputs)
    else:
        inputs = _clean_input(inputs)
        ifunction = pn.bind(function, inputs)

    if outputs:
        if not isinstance(outputs, (list, tuple)):
            outputs = (outputs,)

        outputs = pipe(ifunction, *outputs)
    else:
        outputs = pipe(ifunction)
    return inputs, outputs
