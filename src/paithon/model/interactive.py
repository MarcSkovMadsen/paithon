from typing import Optional
import panel as pn

from .pipe import pipe


def _to_instance(input):
    if callable(input):
        return input()
    return input


def interactive(function, inputs, outputs=None, num_outputs: Optional[int]=None, loading_indicator=False):
    if isinstance(inputs, dict):
        inputs = {key: _to_instance(input) for key, input in inputs.items()}
        ifunction = pn.bind(function, **inputs)
    elif isinstance(inputs, (list, tuple)):
        inputs = tuple(_to_instance(input) for input in inputs)
        ifunction = pn.bind(function, *inputs)
    else:
        inputs = _to_instance(inputs)
        ifunction = pn.bind(function, inputs)

    if outputs:
        if not isinstance(outputs, (list, tuple)):
            outputs = (outputs,)

        outputs = pipe(ifunction, *outputs, loading_indicator=loading_indicator, num_outputs=num_outputs)
    else:
        outputs = pipe(ifunction, loading_indicator=loading_indicator, num_outputs=num_outputs)
    return inputs, outputs
