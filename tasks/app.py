"""Module of tasks for serving the app

"""
import glob

from invoke import task


@task
def serve(command):
    """Serves the test apps

    Arguments:
        command {[type]} -- [description]
    """
    print(
        """
Serves the test apps
====================
"""
    )
    files = " ".join(glob.glob("tests/apps/*.py"))
    command.run(
        f"panel serve {files} --autoreload",
        echo=True,
    )
