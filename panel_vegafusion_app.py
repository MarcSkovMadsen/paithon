import panel as pn
import altair as alt
from vega_datasets import data

pn.extension("ipywidgets", template="fast")

from vegafusion_jupyter import VegaFusionWidget

ACCENT = "#1f77b4"
PALETTE = [ACCENT, "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

import time

import logging
logger = logging.getLogger("vegafusion")

from vega_fusion_jupyter._frontend import module_name, module_version
import altair as alt
import json

from .runtime import runtime


if not "panel-vegafusion" in pn.state.cache:
    seattle_weather = pn.state.cache["panel-vegafusion"]=data.seattle_weather()
else:
    seattle_weather = pn.state.cache["panel-vegafusion"]

def get_chart(seattle_weather):
    brush = alt.selection(type='interval', encodings=['x'])

    bars = alt.Chart().mark_bar().encode(
        x='month(date):O',
        y='mean(precipitation):Q',
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
    ).add_selection(
        brush
    )

    line = alt.Chart().mark_rule(color='firebrick').encode(
        y='mean(precipitation):Q',
        size=alt.SizeValue(3)
    ).transform_filter(
        brush
    )

    return alt.layer(bars, line, data=seattle_weather)

chart = get_chart(seattle_weather)
vchart = VegaFusionWidget(chart)
pn.pane.IPyWidget(vchart).servable()

pn.state.template.param.update(
    site="Vegafusion", title="Interactive Big Data Apps with Crossfiltering",
    accent_base_color=ACCENT, header_background=ACCENT
)