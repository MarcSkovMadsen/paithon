"""Test of the reactive helper functions that makes working with ReactiveHTML easier"""
import pathlib

import pytest

from panel_ai.base.reactive import _clean_script, read_scripts, text_to_scripts

EXAMPLE_SCRIPTS = [
    (  # Reference Example
        """
render=()=>{
  console.log(data)
}
value=()=>{
  my_func(value)
}
""",
        {"render": "console.log(data)", "value": "my_func(value)"},
    ),
    # With and without function arguments
    (
        """
theme=()=>{
    state.chart.updateOptions({theme: {mode: state.tMap(data.theme)}})
}""",
        {"theme": "state.chart.updateOptions({theme: {mode: state.tMap(data.theme)}})"},
    ),
    (
        """
theme=(state)=>{
    state.chart.updateOptions({theme: {mode: state.tMap(data.theme)}})
}""",
        {"theme": "state.chart.updateOptions({theme: {mode: state.tMap(data.theme)}})"},
    ),
    (
        """
theme=(state, data)=>{
    state.chart.updateOptions({theme: {mode: state.tMap(data.theme)}})
}""",
        {"theme": "state.chart.updateOptions({theme: {mode: state.tMap(data.theme)}})"},
    ),
    (
        """
theme=(state,data)=>{
    state.chart.updateOptions({theme: {mode: state.tMap(data.theme)}})
}""",
        {"theme": "state.chart.updateOptions({theme: {mode: state.tMap(data.theme)}})"},
    ),
    # Nested function definitions
    (
        """
render=()=>{
    color=(x)=>{
        return {"x": x["value"]
    }
}""",
        {
            "render": """\
color=(x)=>{
    return {"x": x["value"]
}"""
        },
    ),
]

EXAMPLE_DIRTY_CLEAN_SCRIPTS = [("  console.log(data)\n", "console.log(data)")]

# pylint: disable=line-too-long
TEST_REACTIVE_JS = {
    "after_layout": 'document.addEventListener("click", function(event) {\n    let container_elmnt = document.getElementById(container.id);\n    if (!container_elmnt.contains(event.target) && options.style.display=="block") {\n        options.style.display = "none"\n    }\n});',
    "click_handler": 'if (options.style.display!=="none") {\n    options.style.display="none"\n} else {\n    options.style.display="block"\n}\nview.resize_layout()',
    "key_up_handler": 'if (event.key == "Enter") {\n    data.value = event.target.value\n    options.style.display="none"\n}',
    "options_click_handler": 'let opt_elmnt = event.target.closest(".run_select_option")\ndata.value = opt_elmnt.firstChild.innerHTML\nif (options.style.display!=="none") {\n    options.style.display="none"\n} else {\n    options.style.display="block"\n}\nview.resize_layout()',
    "render": 'options.style.display="none"',
}
# pylint: enable=line-too-long


@pytest.mark.parametrize(["text", "scripts"], EXAMPLE_SCRIPTS)
def test_to_scripts(text, scripts):
    """Test that a javascript string can be converted to the `_scripts` dictionary"""
    assert text_to_scripts(text) == scripts


@pytest.mark.parametrize(["dirty", "clean"], EXAMPLE_DIRTY_CLEAN_SCRIPTS)
def test_clean_script(dirty, clean):
    """Test that a javascript string can be cleaned appropriately"""
    assert _clean_script(dirty) == clean


def test_read_scripts_by_jsname_and_pyfile():
    """Test that a javascript filed can be read and converted appropriately"""
    assert read_scripts(jsfile="test_reactive.js", pyfile=__file__) == TEST_REACTIVE_JS


def test_read_scripts_using_full_path():
    """Test that a javascript filed can be read and converted appropriately"""
    path = pathlib.Path(__file__).parent / "test_reactive.js"
    assert read_scripts(path) == TEST_REACTIVE_JS
