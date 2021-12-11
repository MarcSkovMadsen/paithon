"""The `interactive` function makes your model interactive in no time."""
from typing import Optional, Tuple

import panel as pn
from panel.layout.base import ListLike

from .pipe_to import pipe_to
from .pipe_from import pipe_from

def _to_tuple(outputs) -> Tuple:
    if not outputs:
        return tuple()
    if not isinstance(outputs, (list, tuple)):
        return (outputs,)
    return tuple(outputs)

def interactive(
    model, inputs, outputs=None, num_outputs: Optional[int] = None, loading_indicator=False, default_layout: ListLike=pn.Row, **params
) -> ListLike:
    """Returns input widgets and outputs for your model. The inputs

    Args:
        function ([type]): [description]
        inputs ([type]): [description]
        outputs ([type], optional): [description]. Defaults to None.
        num_outputs (Optional[int], optional): [description]. Defaults to None.
        loading_indicator (bool, optional): [description]. Defaults to False.

    Returns:
        ListLike: A layout of inputs and outputs
    """
    ifunction, inputs = pipe_from(model, inputs)

    outputs = _to_tuple(outputs)
    outputs = pipe_to(
        ifunction, *outputs, loading_indicator=loading_indicator, num_outputs=num_outputs
    )
    return default_layout(inputs, outputs, **params)
