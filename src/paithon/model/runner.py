"""The ModelRunner makes running the model more interactive"""
import logging
import time
from typing import List, Optional

import param
import panel as pn

from .model import Model

logger = logging.getLogger(__name__)


class ModelStats(param.Parameterized):
    """Contains statistics for the number of runs of a Model, the average duration etc."""
    runs = param.Integer(constant=True, doc="""The number of runs
    """)
    duration_total = param.Number(constant=True, doc="""
    The total duration in seconds""")
    duration_avg = param.Number(constant=True, doc="""
    The average duration of a run in seconds""")

    def update(self, duration: float):
        """Use this function to update the stats

        Args:
            duration (float): The duration in seconds of a model run

        Raises:
            ValueError: if the duration provided is negative
        """
        if duration < 0:
            raise ValueError(f"A negative duration is not allowed")
        with param.edit_constant(self):
            self.runs += 1
            self.duration_total += duration
            self.duration_avg = self.duration_total / self.runs

    def reset(self):
        """Resets the stats to zero"""
        self.runs = self.duration_total = self.duration_avg = 0

class ModelRunner(param.Parameterized):
    value = param.ClassSelector(class_=Model, constant=True, doc="""
    The model to run""")
    stats = param.ClassSelector(class_=ModelStats, constant=True, doc="""
    Holds the stats like number of runs""")

    kwargs = param.Dict(constant=True, doc="""
    The arguments (parameter: value) of the last run""")
    result = param.Parameter(constant=True, doc="""
    The result of the last run""")

    run = param.Action(doc="""
    Method to run the model. You can it with both positional and keyword arguments.""")
    active = param.Boolean(doc="""True while the running the model. False otherwise.""")

    submit = param.Event(doc="""Set this to True to submit a run with the current values of the
    Model.""")
    auto_submit = param.Boolean(default=True, doc="""If True the model is automatically run when a
    parameter of the Model changes. If False you need to manually `submit` to run the model""")

    outputs = param.List(constant=True, doc="""
    A List of panes to pipe the result to""")

    def __init__(self, value: Model, auto_submit: bool=True, outputs: Optional[List]=None, initial_run=False):
        if not outputs:
            outputs=[]
        super().__init__(value=value, auto_submit=auto_submit, outputs=outputs, stats=ModelStats())
        self.run = self._run
        self._watchers = self._setup_watchers(initial_run=initial_run)

    def _run(self, *args, **kwargs):
        self.active = True
        start = time.time()
        result = self.value(*args, **kwargs)
        kwargs = self.value.kwargs
        end = time.time()

        self._update_outputs(result)
        self.stats.update(end - start)
        with param.edit_constant(self):
            self.kwargs = kwargs
            self.result = result
        self.active = False
        return result

    def _update_outputs(self, result):
        if self.outputs:
            if len(self.outputs) == 1:
                self.outputs[0].object = result
            else:
                for result, output in zip(result, self.outputs):
                    output.object = result

    @param.depends("value", watch=True)
    def _reset_stats(self):
        self.stats.reset()

    @param.depends("submit", watch=True)
    def _handle_submit(self):
        self.run()

    def create_submit_button(
        self, name="SUBMIT", width=100, sizing_mode="fixed", button_type="primary", **params
    ) -> pn.widgets.Button:
        """Returns a Button. When clicked the button submits a run.

        Args:
            name (str, optional): The name of the Button. Defaults to "SUBMIT".
            width (int, optional): The width of the Button. Defaults to 100.
            sizing_mode (str, optional): The sizing_mode of the button. Defaults to "fixed".
            button_type (str, optional): The type of the button. Defaults to "primary".

        Returns:
            pn.widgets.Button: A button to submit runs
        """
        button = pn.widgets.Button.from_param(
            self.param.submit,
            name=name,
            width=width,
            sizing_mode=sizing_mode,
            button_type=button_type,
            **params,
        )

        def _handle_autosubmit_changed(value):
            button.visible = not value
        _handle_autosubmit_changed(self.auto_submit)
        pn.bind(_handle_autosubmit_changed, value=self.param.auto_submit)

        return button

    def _setup_watchers(self, initial_run=True):
        logging.debug("_setup_watchers start")
        clean_model = self.value
        watchers = []

        def handle_parameter_changed(*events):
            if not self.auto_submit:
                return

            args = [
                getattr(clean_model, parameter) for parameter in clean_model._function_parameters
            ]
            self.run(*args)

        if initial_run:
            self.run()

        for parameter in clean_model._function_parameters:
            watcher = clean_model.param.watch(handle_parameter_changed, parameter)
            watchers.append(watcher)
        return watchers
