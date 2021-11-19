"""This module contains functionality to view docstrings of Parameterized Classes
"""
import ansiconv
import panel as pn
import param
from param.parameterized import edit_constant

from panel_ai.base.component import extract_layout_parameters


class DocStringViewer(pn.viewable.Viewer):
    """The DocStringViewer makes viewing the docstring of a Parameterized class easy and
    beautiful"""

    object = param.ClassSelector(
        class_=param.Parameterized,
        doc="""
    The Parameterized class to view
    """,
    )
    theme = param.Selector(
        default="default",
        objects=["default", "dark"],
        constant=True,
        doc="""
    The theme of the component: 'default' or 'dark.""",
    )
    _html = param.String(constant=True)

    def __init__(self, **params):
        params, layout_params = extract_layout_parameters(params)
        if "theme" not in params:
            if pn.state.session_args and "theme" in pn.state.session_args:
                theme = pn.state.session_args.get("theme")[0].decode()
                if theme == "dark":
                    params["theme"] = theme
        super().__init__(**params)

        self._html_pane = pn.pane.HTML(sizing_mode="stretch_both")
        self.layout = pn.Column(self._html_pane, scroll=True, **layout_params)
        self._update_html()

    def __panel__(self):
        return self.layout

    @param.depends("object", "theme", watch=True)
    def _update_html(self):
        with edit_constant(self):
            self._html = self._to_html(self.object.__doc__, self.theme)

    @param.depends("_html", watch=True)
    def _update_html_pane(self):
        self._html_pane.object = self._html

    @classmethod
    def _to_html(cls, txt, theme):
        if not txt:
            return ""
        html = ansiconv.to_html(txt)
        css = ansiconv.base_css()
        if theme == "dark":
            css = cls._get_css(red="#ff8b8b", green="#8bFF8b", blue="#66b3ff")
        else:
            css = cls._get_css(
                background="#FFFFFF",
                color="#000000",
                red="#8E0500",
                green="#19AF22",
                blue="#00008b",
                cyan="#17625F",
            )

        html = f"""
        <style>{css}</style>
        <pre class="ansi_fore ansi_back">{html}</pre>
        """
        return html

    @staticmethod
    def _get_css(  # pylint: disable=too-many-arguments
        background="#000000",
        color="#FFFFFF",
        red="#FF0000",
        green="#00FF00",
        blue="#0000FF",
        cyan="#00FFFF",
    ):
        return f"""
    .ansi_fore {{ color: {color}; }}
    .ansi_back {{ background-color: inherit; padding: 20px; border-radius: 4px; opacity: 0.8 }}
    .ansi1 {{ font-weight: bold; }}
    .ansi3 {{ font-weight: italic; }}
    .ansi4 {{ text-decoration: underline; }}
    .ansi9 {{ text-decoration: line-through; }}
    .ansi30 {{ color: {background}; }}
    .ansi31 {{ color: {red}; }}
    .ansi32 {{ color: {green}; }}
    .ansi33 {{ color: #FFFF00; }}
    .ansi34 {{ color: {blue}; }}
    .ansi35 {{ color: #FF00FF; }}
    .ansi36 {{ color: {cyan}; }}
    .ansi37 {{ color: {color}; }}
    .ansi40 {{ background-color: {background}; }}
    .ansi41 {{ background-color: {red}; }}
    .ansi42 {{ background-color: {green}; }}
    .ansi43 {{ background-color: #FFFF00; }}
    .ansi44 {{ background-color: {blue}; }}
    .ansi45 {{ background-color: #FF00FF; }}
    .ansi46 {{ background-color: {cyan}; }}
    .ansi47 {{ background-color: {color}; }}
    """


DocStringViewer()
