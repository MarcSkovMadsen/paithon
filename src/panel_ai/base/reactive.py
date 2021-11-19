"""Module for making the developer experience for ReactiveHTML
event better
"""
import pathlib
import textwrap
from typing import Dict


def _clean_script(value):
    return textwrap.dedent(value).strip()


def text_to_scripts(text: str) -> Dict:
    """Returns a `_scripts` dictionary for ReactiveHTML based on a string

    Args:
        text (str): The input string

    Returns:
        Dict: The output `_scripts`

    Example:

    >>> txt='''
    ... render=()=>{
    ...   console.log(data)
    ... }
    ... value=()=>{
    ...   my_func(value)
    ... }
    ... '''
    >>> text_to_scripts(txt)
    {'render': 'console.log(data)', 'value': 'my_func(value)'}
    """
    lines = text.split("\n")
    scripts = {}
    key = ""
    value = ""
    for line in lines:
        if key:
            if line == "}":
                scripts[key] = _clean_script(value)
                key = value = ""
            else:
                value += line + "\n"
        else:
            if line and not line[0] == " " and line.endswith(")=>{") and "=(" in line:
                key = line.split("=")[0]

    return scripts


def read_scripts(jsfile: str = "", pyfile: str = "") -> dict:
    """Reads a `.js` file and converts it to a _scripts dictionary

    Args:
        jsfile (Union[str,pathlib.Path], optional): The path or name of the file.
        pyfile (str, optional): Optional __file__ of the .py file file.
            If provided its assumed the jsfile is in the same folder as pyfile

    Returns:
        dict: A dictionary of _scripts for a ReactiveHTML _template
    """
    if pyfile:
        full_path = pathlib.Path(pyfile).parent / jsfile
    else:
        full_path = pathlib.Path(jsfile)

    with open(full_path, "r", encoding="utf8") as _file:
        text = _file.read()
    return text_to_scripts(text)
