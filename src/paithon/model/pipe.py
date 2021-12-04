"""The pipe makes it possible to pipe the output(s) of function bound to parameters or widgets to
specific panes.
"""
from itertools import zip_longest
from typing import Any, Callable, List, Tuple, Union

import panel as pn
import param

from .pipe_class import pipe as _get_pipe


def _validate_function(function):
    if not hasattr(function, "__wrapped__") or not hasattr(function, "_dinfo"):
        raise ValueError(
            "Function has not been bound. Please apply panel.bind before using the pipe"
        )


def _create_pipes(results, outputs):
    if not isinstance(results, tuple):
        raise ValueError("results is not tuple")
    if not isinstance(outputs, tuple):
        raise ValueError("outputs is not a tuple")
    return tuple(_get_pipe(output=output, object=result) for result, output in zip_longest(results, outputs))

def pipe(function: Callable, *outputs, default_layout=pn.Column, loading_indicator=True) -> Union[Any, Tuple]:
    """Returns an instantiated and bound version of the outputs

    If no outputs are provided then outputs will be inferred from from the first return value
    of the function. If an iterable is returned the number of outputs is inferred from its length.

    Args:
        function (Callable): A bound function. It's return values will be piped to the outputs
        outputs (Parameterized): One or more Parameterized classes or instances with an `object`
        or `value` parameter. For example panes, widgets, indicators and your own custom outputs.

    Raises:
        ValueError: Raised if 1) the function is not bound to inputs or 2) the outputs specified
        are not Parameterized classes with and object or value parameter like for example a
        widget, indicator or pane.

    Returns:
        Union[Any, Tuple[Any]]: A single output or tuple of outputs
    """
    _validate_function(function)

    inputs = tuple(function._dinfo["kw"].values())  # type: ignore[attr-defined] pylint: disable=protected-access
    pipes = None

    def _get_results() -> Tuple:
        if pipes:
            for _pipe in pipes:
                _pipe.loading=True and loading_indicator
        args = tuple(getattr(input.owner, input.name) for input in inputs)
        kwargs = dict(zip(function._dinfo["kw"].keys(), args))  # type: ignore[attr-defined] pylint: disable=protected-access
        results = function(**kwargs)
        if not isinstance(results, (list, tuple)):
            results = (results,)
        return tuple(results)

    def _set_result(results: tuple, *pipes):
        for index, _pipe in enumerate(pipes):
            _pipe.object = results[index]
            _pipe.loading = False

    results = _get_results()
    pipes = _create_pipes(results, outputs)
    outputs = tuple(pipe.output for pipe in pipes)

    def _handle_change(*events):
        results = _get_results()
        _set_result(results, *pipes)


    for _input in inputs:
        _input.owner.param.watch(_handle_change, parameter_names=[_input.name])
    if len(outputs) == 1:
        return outputs[0]
    if callable(default_layout):
        default_layout = default_layout()
    default_layout[:]=list(outputs)
    return default_layout
