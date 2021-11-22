"""This module contains functionality to view docstrings of Parameterized Classes
"""
import ansiconv
import panel as pn
import param

from ...base.component import extract_layout_parameters, get_theme

# Inspiration at https://iterm2colorschemes.com/
ANSI_THEMES = {
    "Solarized": {  # https://ethanschoonover.com/solarized/
        "default": {
            "background": "#fdf6e3",  # Background
            "color": "#657b83",  # Text
            "red": "#cb4b16",  # Parameters changed, 2nd row in table
            "green": "#859900",  # heading
            "blue": "#268bd2",  # Table Header, 1st row in table
            "cyan": "#2aa198",  # soft bound values
        },
        "dark": {
            "background": "#002b36",
            "color": "#839496",
            "red": "#cb4b16",
            "green": "#859900",
            "blue": "#268bd2",
            "cyan": "#2aa198",  # soft bound values
        },
    },
    "Tomorrow": {  # https://github.com/chriskempson/tomorrow-theme
        "default": {
            "background": "inherit",  # "#ffffff",
            "color": "#4d4d4c",  # Foreground
            "red": "#c82829",
            "green": "#718c00",
            "blue": "#4271ae",
            "cyan": "#3e999f",  # aqua
        },
        "dark": {
            "background": "inherit",  # "#1d1f21",
            "color": "#c5c8c6",
            "red": "#cc6666",
            "green": "#b5bd68",
            "blue": "#81a2be",
            "cyan": "#2aa198",
        },
    },
}


class DocStringViewer(pn.viewable.Viewer):
    """The DocStringViewer makes viewing the docstring of a Parameterized class easy and
beautiful.
"""

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
    palette = param.Selector(
        default="Tomorrow",
        objects=ANSI_THEMES.keys(),
        doc="""
    For example `solarized`.
    """,
    )
    _html = param.String(
        constant=True,
        doc="""
    The html representation of the doc string
    """,
    )

    def __init__(self, object=None, **params):  # pylint: disable=abstract-method, redefined-builtin
        params, layout_params = extract_layout_parameters(params)
        if "theme" not in params:
            params["theme"] = get_theme()
        if object:
            params["object"] = object
        super().__init__(**params)
        self._html_pane = pn.pane.HTML(sizing_mode="stretch_both")
        if "scroll" not in layout_params:
            layout_params["scroll"] = True
        self.layout = pn.Column(self._html_pane, **layout_params)
        self._update_html()

    def __panel__(self):
        return self.layout

    @param.depends("object", "theme", "palette", watch=True)
    def _update_html(self):
        with param.edit_constant(self):
            doc = self.object.__doc__
            if doc:
                doc = "\n".join(doc.split("\n")[1:])
            else:
                doc = ""
            self._html = self._to_html(doc, self.theme, self.palette)

    @param.depends("_html", watch=True)
    def _update_html_pane(self):
        self._html_pane.object = self._html

    @classmethod
    def _to_html(cls, txt, theme, palette):
        if not txt:
            return ""
        html = ansiconv.to_html(txt)
        css = cls._get_css(**ANSI_THEMES[palette][theme])
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
    .ansi_back {{ background-color: {background}; padding: 20px; height:100%; border-radius: 4px; opacity: 0.8;font: 1rem Inconsolata, monospace; }}
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
