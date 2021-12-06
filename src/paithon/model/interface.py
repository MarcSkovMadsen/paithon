"""Provides an easy to use interface for you model(s)."""
import logging
from typing import Any, Optional

import panel as pn
import param

from ..shared.widgets.screenshot import Screenshot
from .api import ModelApi
from .model import Model
from .runner import ModelRunner
from .view import InterfaceView

logger = logging.getLogger(__name__)


class Interface(param.Parameterized):
    """Make your AI `model` interactive by providing

    - your `model`
    - a list of `inputs` consisting of widgets
    - a list of `outputs` consisting of panes"""

    name: str = param.String(doc="""The name of the model""")
    description: str = param.String(doc="""A short summary descripion of the model""")
    article: str = param.String(doc="""A longer article. Supports Markdown""")

    model = param.Parameter(
        doc="""
    A callable that 1) takes values of the specified inputs and 2) and outputs a result that can be
    visualized by the specified outputs."""
    )
    inputs = param.Parameter(
        constant=True,
        doc="""
        A dictionary of parameter names and widgets providing the arguments to the model.""",
    )
    outputs = param.Parameter(
        constant=True,
        doc="""
        A list of components visualizing the output of the model.""",
    )

    arguments = param.List()
    result = param.List()

    submit = param.Event()

    screenshot = param.Event()
    screenshot_disabled = param.Boolean(
        default=False,
        doc="""
    If True the screenshot button will be hidden.""",
    )

    flag = param.Event()
    flag_options = param.List()
    flag_disabled = param.Boolean(
        default=False,
        doc="""
    If True the flag button will not be visible. """,
    )

    view = param.ClassSelector(class_=InterfaceView)
    api = param.ClassSelector(class_=ModelApi)

    def __init__(  # pylint: disable=too-many-arguments)
        self,
        model: Model,
        inputs: Optional[Any] = None,
        outputs: Optional[Any] = None,
        auto_submit: bool = True,
        initial_run: bool = True,
        **params,
    ):
        clean_model = self._clean_model(model)
        clean_inputs = self._clean_inputs(inputs, clean_model)
        clean_outputs = self._clean_outputs(outputs)
        model_runner = ModelRunner(
            value=clean_model,
            outputs=clean_outputs,
            auto_submit=auto_submit,
            initial_run=initial_run,
        )

        screenshot = Screenshot(
            height=0,
            width=0,
            margin=0,
        )
        screenshot_button = pn.widgets.Button.from_param(
            screenshot.param.take, button_type="default", width=100, sizing_mode="fixed"
        )
        submit_button = model_runner.create_submit_button()
        input_tools = [submit_button]
        output_tools = [screenshot_button, screenshot]

        params["view"] = InterfaceView(
            model=clean_model,
            inputs=clean_inputs,
            input_tools=input_tools,
            outputs=clean_outputs,
            output_tools=output_tools,
        )
        params["api"] = ModelApi()
        super().__init__(model=model, inputs=inputs, outputs=outputs, **params)

    @staticmethod
    def _clean_model(model):
        if isinstance(model, Model):
            return model
        if issubclass(model, Model):
            return model.instance()
        raise TypeError(f"{type(model)} is not a supported model type")

    @classmethod
    def _clean_inputs(cls, inputs, model: Model):
        if inputs is None:
            inputs = {}

        # pylint: disable=protected-access
        col = pn.Param(model, parameters=model._function_parameters, widgets=inputs)
        return {key: col[index + 1] for index, key in enumerate(model._function_parameters)}

    @classmethod
    def _clean_outputs(cls, outputs):
        if not isinstance(outputs, list):
            return [cls._clean_output(outputs)]
        return [cls._clean_output(output) for output in outputs]

    @classmethod
    def _clean_output(cls, output):
        if isinstance(output, param.Parameterized):
            return output
        if issubclass(output, param.Parameterized):
            return output()
        raise TypeError(f"Output {output} is not a Parameterized instance or class")

    @staticmethod
    def _is_class(output):
        return issubclass(output, param.Parameterized)
