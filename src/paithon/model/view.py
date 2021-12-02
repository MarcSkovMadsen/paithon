from typing import Dict, List

import panel as pn
import param

from .model import Model


class ModelView(pn.viewable.Viewer):
    model: Model = param.ClassSelector(
        class_=Model,
        constant=True,
        doc="""
    A callable that 1) takes values of the specified inputs and 2) and outputs a result that can be
    visualized by the specified outputs.""",
    )
    inputs: Dict = param.Dict(
        constant=True,
        doc="""
        A dictionary of parameter names and widgets providing the arguments to the model.""",
    )
    input_tools = param.List()
    outputs: List = param.List(
        constant=True,
        doc="""
        A list of components visualizing the output of the model.""",
    )
    output_tools = param.List()

    def __init__(self, **params):
        super().__init__(**params)

        output_header = pn.pane.Markdown("# Outputs ")

        input_divider = pn.Spacer(
            height=2, background="lightgray", sizing_mode="stretch_width", margin=(-10, 0, 25, 0)
        )
        output_divider = pn.Spacer(
            height=2, background="lightgray", sizing_mode="stretch_width", margin=(-10, 0, 25, 0)
        )
        input_output_divider = pn.layout.Spacer(
            width=2, background="lightgray", sizing_mode="stretch_height", margin=(0, 25)
        )
        self._layout = pn.Row(
            pn.Column(
                pn.Row(pn.pane.Markdown("# Inputs"), pn.Spacer(), *self.input_tools),
                input_divider,
                *self.inputs.values(),
            ),
            input_output_divider,
            pn.Column(
                pn.Row(output_header, pn.Spacer(), *self.output_tools),
                output_divider,
                *self.outputs,
            ),
            margin=(10, 100),
        )

    def __panel__(self):
        return self._layout
