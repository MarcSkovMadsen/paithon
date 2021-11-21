import panel as pn
import param

class MyElement(pn.reactive.ReactiveHTML):
    data_url = param.String("abcd")
    _template = """<div id="component">Hi</div>"""
    _scripts = {
        "render": """dt={data_url: "abcd};dt.data_url="123";"""
    }

MyElement().servable()
