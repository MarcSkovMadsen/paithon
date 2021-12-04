import panel as pn

pn.extension(sizing_mode="stretch_width")


def data(n):
    return {index: index for index in range(n)}


slider = pn.widgets.IntSlider(value=0, start=0, end=100)
idata = pn.bind(data, slider)
pn.Column(slider, idata, "Something else").servable()
