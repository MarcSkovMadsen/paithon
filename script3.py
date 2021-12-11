import panel as pn
import param
import hvplot.pandas

pn.extension(sizing_mode="stretch_width")

ACCENT_COLOR="#D2386C"

CSS = """
.before-after-container {
    position: relative;
    height:100%;
    width:100%
    border: 2px solid white;
}
.before-after-container .img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.before-after-container .slider {
    position: absolute;
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 100%;
    outline: none;
    margin: 0;
    transition: all 0.2s;
    display: flex;
    justify-content: center;
    align-items: center;
    --track-width: 0;
}
.before-after-container .slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 12px;
    height: 99%;
    background: silver;
    cursor: pointer;
    border-radius: 8px
}
.before-after-container .slider::-moz-range-thumb {
    width: 12px;
    height: 99%;
    background: silver;
    cursor: pointer;
    border-radius: 8px
}
.before-after-container .slider-button {
    pointer-events: none;
    position: absolute;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: silver;
    left: calc(50% - 18px);
    top: calc(50% - 18px);
    display: flex;
    justify-content: center;
    align-items: center;
}
.before-after-container .slider-button:after {
    content: '';
    padding: 3px;
    display: inline-block;
    border: solid #5d5d5d;
    border-width: 0 2px 2px 0;
    transform: rotate(-45deg);
}
.before-after-container .slider-button:before {
    content: '';
    padding: 3px;
    display: inline-block;
    border: solid #5d5d5d;
    border-width: 0 2px 2px 0;
    transform: rotate(135deg);
}
"""

pn.config.raw_css.append(CSS)

class BeforeAfterLayout(pn.reactive.ReactiveHTML):
    value = param.Integer(50, bounds=(0,100))
    left2 = param.Parameter(allow_None=False)
    right2 = param.Parameter(allow_None=False)


    _template = """
<div id="container" class='before-after-container'>
    <div id="right" class='img background-img' style="height:100%;">
        <div id="right_inner" style="height:100%;">${right2}</div>
    </div>
    <div id="left" class='img foreground-img' style="height:100%;overflow:hidden">
        <div id="left_inner" style="height:100%">${left2}</div>
    </div>
    <input type="range" min="1" max="100" value="${value}" class="slider" name='slider' id="slider" oninput="${script('handle_change')}"></input>
</div>
"""

    _scripts = {
        "render": """
console.log(left)
state.right_inner=right.children[0]
state.left_inner=left.children[0]
function setImageWidth(){
    width=view.el.offsetWidth-12
    state.left_inner.style.width=`${width}px`
    state.right_inner.style.width=`${width}px`
}
setImageWidth()
window.addEventListener("resize", setImageWidth);

adjustment = parseInt((100-data.value)/100*18)
left.style.width=`calc(${data.value}% - ${adjustment}px)`
""",
        "handle_change": """
const sliderPos = parseInt(event.target.value);
adjustment = parseInt((100-sliderPos)/100*18)
left.style.width=`calc(${sliderPos}% - ${adjustment}px)`
data.value=parseInt(sliderPos)
""",
        "value": """
const sliderPos = data.value
adjustment = parseInt((100-data.value)/100*18)
left.style.width=`calc(${sliderPos}% - ${adjustment}px)`
"""
    }

import pandas as pd
data = pd.DataFrame({"y": range(10)})
left = data.hvplot().opts(color="red", line_width=6, responsive=True, height=700)
right = data.hvplot().opts(color="green", line_width=6, responsive=True, height=700)

before_after = BeforeAfterLayout(
    value=20,left2=left,right2=right, height=800
)
controls = pn.Param(before_after, parameters=["value"])
pn.template.FastListTemplate(
    site="Awesome Panel", title="Image Slider",
    sidebar=[controls], main=[before_after],
    accent_base_color=ACCENT_COLOR, header_background=ACCENT_COLOR
).servable()