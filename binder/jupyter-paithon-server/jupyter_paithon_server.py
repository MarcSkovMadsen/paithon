"""
Function to configure serving the panel example apps via jupyter-server-proxy.
"""
import pathlib
from glob import glob

ICON_PATH = str((pathlib.Path(__file__).parent / "paithon-apps-icon.svg").absolute())


def panel_serve_examples():
    """Returns the jupyter-server-proxy configuration for serving the example notebooks as Panel
    apps.

    Returns:
        Dict: The configuration dictionary
    """
    # See:
    # https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
    # https://github.com/holoviz/jupyter-panel-proxy/blob/master/panel_server/__init__.py
    return {
        "command": [
            "panel",
            "serve",
            *glob("examples/*.ipynb", recursive=True),
            "--allow-websocket-origin=*",
            "--port",
            "{port}",
            "--prefix",
            "{base_url}panel",
        ],
        "absolute_url": True,
        "timeout": 360,
        "launcher_entry": {
            "enabled": True,
            "title": "Paithon Apps",
            "icon_path": ICON_PATH,
        },
    }
