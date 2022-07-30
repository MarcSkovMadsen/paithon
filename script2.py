import panel as pn
import datetime

template = """
This page was created {{ asof }}
"""

tmpl = pn.Template(template)
tmpl.add_variable('asof', datetime.datetime.now())

tmpl.servable()
