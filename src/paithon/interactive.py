from typing import Any, Callable, Dict, List, Optional, Union
import time
import panel as pn
import param
from panel.layout.base import ListLike

from .shared.widgets.screenshot import Screenshot


from param import ParamOverrides

class RunStats(param.Parameterized):
    runs = param.Integer(constant=True)
    duration_total = param.Number(constant=True)
    duration_avg = param.Number(constant=True)

    def update(self, duration: float):
        if duration<0:
            raise ValueError(f"A negative duration is not allowed")
        with param.edit_constant(self):
            self.runs+=1
            self.duration_total+=duration
            self.duration_avg=self.duration_total/self.runs

    def reset(self):
        self.runs=self.duration_total=self.duration_avg=0

class Model(param.ParameterizedFunction):
    runs = param.ClassSelector(class_=RunStats)

    _non_function_parameters = ["name", "runs"]

    _function = None

    @property
    def _function_parameters(self):
        return [
            parameter for parameter in self.param if not parameter in self._non_function_parameters
        ]

    def __call__(self, *args, **params):
        params = self._to_params(*args, **params)
        return self._function(**params)

    def _to_params(self, *args, **params):
        args_params = {}
        for index, value in enumerate(args):
            key = self._function_parameters[index]
            args_params[key] = value
        params = {**args_params, **params}

        p = ParamOverrides(self, params)
        return {key: p[key] for key in self._function_parameters}

    @property
    def kwargs(self):
        return self._to_params()

class ModelRunner(param.Parameterized):
    value = param.ClassSelector(class_=Model)
    stats = param.ClassSelector(class_=RunStats, constant=True)

    kwargs = param.Dict(constant=True)
    result = param.Parameter(constant=True)

    run = param.Action()

    def __init__(self, value: Model):
        super().__init__(value=value, stats=RunStats())

        self.run = self._run

    def _run(self, *args, **kwargs):
        start = time.time()
        result = self.value(*args, **kwargs)
        kwargs=self.value.kwargs
        end = time.time()
        self.stats.update(end-start)

        with param.edit_constant(self):
            self.kwargs=kwargs
            self.result=result
        return result

    @param.depends("value", watch=True)
    def _reset_stats(self):
        self.stats.reset()

class InteractiveView(pn.viewable.Viewer):
    model: Model = param.ClassSelector(class_=Model, constant=True, doc="""
    A callable that 1) takes values of the specified inputs and 2) and outputs a result that can be
    visualized by the specified outputs.""")
    inputs: Dict = param.Dict(constant=True, doc="""
        A dictionary of parameter names and widgets providing the arguments to the model.""")
    input_tools = param.List()
    outputs: List = param.List(constant=True, doc="""
        A list of components visualizing the output of the model.""")
    output_tools = param.List()

    def __init__(self, **params):
        super().__init__(**params)

        output_header = pn.pane.Markdown("# Outputs ")

        input_divider = pn.Spacer(height=2, background="lightgray", sizing_mode="stretch_width", margin=(-10, 0, 25, 0))
        output_divider = pn.Spacer(height=2, background="lightgray", sizing_mode="stretch_width", margin=(-10, 0, 25, 0))
        input_output_divider = pn.layout.Spacer(width=2, background="lightgray", sizing_mode="stretch_height", margin=(0,25))
        self._layout = pn.Row(
            pn.Column(pn.Row(pn.pane.Markdown("# Inputs"), pn.Spacer(), *self.input_tools), input_divider, *self.inputs.values(),),
            input_output_divider,
            pn.Column(pn.Row(output_header, pn.Spacer(), *self.output_tools), output_divider, *self.outputs), margin=(10,100)
        )

    def __panel__(self):
        return self._layout


class InteractiveApi(param.Parameterized):
    def post(self):
        pass

class Interactive(param.Parameterized):
    """Make your AI `model` interactive by providing

- your `model`
- a list of `inputs` consisting of widgets
- a list of `outputs` consisting of panes
"""
    name: str = param.String(doc="""The name of the model""")
    description: str = param.String(doc="""A short summary descripion of the model""")
    article: str = param.String(doc="""A longer article. Supports Markdown""")

    model= param.Parameter(doc="""
    A callable that 1) takes values of the specified inputs and 2) and outputs a result that can be
    visualized by the specified outputs.""")
    inputs = param.Parameter(constant=True, doc="""
        A dictionary of parameter names and widgets providing the arguments to the model.""")
    outputs = param.Parameter(constant=True, doc="""
        A list of components visualizing the output of the model.""")

    arguments = param.List()
    result = param.List()

    submit = param.Event()
    submit_disabled = param.Boolean(default=True, doc="""
    If True the model will be evaulated only when submit is triggered. If False the model will
    be evaluated every time the value of an input is changed.
    """)

    screenshot = param.Event()
    screenshot_disabled = param.Boolean(default=False, doc="""
    If True the screenshot button will be hidden.""")

    flag = param.Event()
    flag_options = param.List()
    flag_disabled = param.Boolean(default=False, doc="""
    If True the flag button will not be visible. """)

    view = param.ClassSelector(class_=InteractiveView)
    api = param.ClassSelector(class_=InteractiveApi)

    def __init__(self, model: Model, inputs: Optional[Any]=None, outputs: Optional[Any]=None, **params):
        clean_model = self._clean_model(model)
        clean_inputs = self._clean_inputs(inputs, clean_model)
        clean_outputs = self._clean_outputs(outputs)

        submit_button=pn.widgets.Button(name="Submit", sizing_mode="fixed", width=100, button_type="primary")
        input_tools=[submit_button]

        self._watchers = self._setup_watchers(clean_model, submit_button, clean_outputs)

        screenshot=Screenshot(height=0, width=0,margin=0,)
        screenshot_button = pn.widgets.Button.from_param(screenshot.param.take, button_type="default", width=100, sizing_mode="fixed")
        output_tools = [screenshot_button, screenshot]

        params["view"]=InteractiveView(
            model=clean_model,
            inputs=clean_inputs,
            input_tools=input_tools,
            outputs=clean_outputs,
            output_tools=output_tools,
        )
        params["api"]=InteractiveApi()
        super().__init__(model=model, inputs=inputs, outputs=outputs, **params)

    def _clean_model(self, model):
        if isinstance(model, Model):
            return model
        if issubclass(model, Model):
            return model.instance()
        raise TypeError(f"{type(model)} is not a supported model type")

    @classmethod
    def _clean_inputs(cls, inputs, model: Model):
        if inputs is None:
            inputs={}

        col = pn.Param(model,parameters=model._function_parameters,widgets = inputs)
        return {
            key: col[index+1] for index, key in enumerate(model._function_parameters)
        }

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

    def _setup_watchers(self, clean_model: Model, submit_button, clean_outputs):
        watchers = []

        def handle_parameter_changed(*events):

            args = [getattr(clean_model, parameter) for parameter in clean_model._function_parameters]
            results = clean_model(*args)
            if len(clean_outputs)==1:
                clean_outputs[0].object = results
            else:
                for result, output in zip(results, self.outputs):
                    output.object = result


            # output_header.object = f"# Outputs: {duration:.2f}s"

        handle_parameter_changed()

        for parameter in clean_model._function_parameters:
            watcher = clean_model.param.watch(handle_parameter_changed, parameter)
            watchers.append(watcher)
        return watchers