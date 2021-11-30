import gradio as gr
import tensorflow as tf
import numpy as np
import requests
import time


inception_net = tf.keras.applications.InceptionV3() # load the model

# Download human-readable labels for ImageNet.
response = requests.get("https://git.io/JJkYN")
labels = response.text.split("\n")

def classify_image(inp):
    if not inp:
        return []
    inp2 = numpy_array_from_data_uri(inp, shape=(299,299)) # inp1.reshape((-1, 299, 299, 3))
    inp2=inp2.reshape((-1, 299, 299, 3))
    inp3 = tf.keras.applications.inception_v3.preprocess_input(inp2)
    prediction = inception_net.predict(inp3).flatten()
    bla= [{"label": labels[i], "score": float(prediction[i])} for i in range(1000)]
    bla = sorted(bla, key=lambda x: -x["score"])
    return bla

import panel as pn
from paithon.image.widgets import ImageInput
from paithon.image.base.pillow import numpy_array_from_data_uri
from paithon.shared.pane import Label
from paithon.shared.widgets import Screenshot
pn.extension(sizing_mode="stretch_width")
image_input = ImageInput(height=800)

inputs = [image_input]
model = classify_image
outputs = [Label(height=800)]

submit_button=pn.widgets.Button(name="Submit", sizing_mode="fixed", width=100, button_type="primary")
input_tools=[submit_button]
screenshot=Screenshot(height=0, width=0,margin=0,)
screenshot_button = pn.widgets.Button.from_param(screenshot.param.take, button_type="default", width=100, sizing_mode="fixed")
output_header = pn.pane.Markdown("# Outputs ")
output_tools = [screenshot_button, screenshot]
watchers = []

def update(*events):
    start = time.time()

    args = [input.uri for input in inputs]
    results = model(*args)
    if len(outputs)==1:
        outputs[0].object = results
    else:
        for result, output in zip(results, outputs):
            output.object = result

    end = time.time()
    duration = end-start
    output_header.object = f"# Outputs: {duration:.2f}s"
update()

for input in inputs:
    watcher = input.param.watch(update, 'uri')
    watchers.append(watcher)

input_divider = pn.Spacer(height=2, background="lightgray", sizing_mode="stretch_width", margin=(-10, 0, 25, 0))
output_divider = pn.Spacer(height=2, background="lightgray", sizing_mode="stretch_width", margin=(-10, 0, 25, 0))
input_output_divider = pn.layout.Spacer(width=2, background="lightgray", sizing_mode="stretch_height", margin=(0,25))

pn.Row(
    pn.Column(pn.Row(pn.pane.Markdown("# Inputs"), pn.Spacer(), *input_tools), input_divider, *inputs,),
    input_output_divider,
    pn.Column(pn.Row(output_header, pn.Spacer(), *output_tools), output_divider, *outputs), margin=(10,100)
).servable()
