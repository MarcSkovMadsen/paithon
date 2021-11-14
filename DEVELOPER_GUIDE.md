# For Contributers

## Prerequisites

- Python>=3.7

## Installation

```bash
git clone https://github.com/marcskovmadsen/panel-ai
cd panel-ai
```

Create your virtual environment.

```bash
python -m venv .venv
```

Activate your virtual environment. On Windows with Git Bash it can be done via

```bash
source .venv/Scripts/activate
```

Install the `panel-ai` package for editing

```bash
pip install -e .[all]
```

Install the [Panel Jupyter Preview](https://blog.holoviz.org/panel_0.12.0.html#JupyterLab-previews)

```bash
jupyter serverextension enable panel.io.jupyter_server_extension
```

## Tests

```bash
invoke test.all
```

will run `isort`, `autoflake`, `black`, `pylint`, `mypy` and `pytest`. It should look like

```bash
$ invoke test.all

Running isort the Python code import sorter
===========================================

isort .
Skipped 7 files

Running autoflake to remove unused imports on all .py files recursively
=======================================================================

autoflake --imports=pytest,pandas,numpy,plotly,dash,urllib3 --in-place --recur
sive .

Running Black the Python code formatter
=======================================

black .
All done! \u2728 \U0001f370 \u2728
16 files left unchanged.

Running pylint.
Pylint looks for programming errors, helps enforcing a coding standard,
sniffs for code smells and offers simple refactoring suggestions.
=======================================================================

pylint setup.py tasks panel_ai tests

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)


Running mypy for identifying python type errors
===============================================

mypy setup.py tasks panel_ai tests
Success: no issues found in 16 source files

Running pytest the test framework
=================================

pytest tests --doctest-modules --cov=panel_ai -m "not functionaltest a
nd not integrationtest" --cov-report html:test_results/cov_html
============================= test session starts =============================
platform win32 -- Python 3.8.4, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: C:\repos\private\panel-ai, configfile: pytest.ini, testpaths: tests
plugins: anyio-2.2.0, cov-2.11.1
collected 6 items

tests\test_config.py .                                                   [ 16%]
tests\test_highchart.py ...                                              [ 66%]
tests\models\test_highchart.py ..                                        [100%]

----------- coverage: platform win32, python 3.8.4-final-0 -----------
Coverage HTML written to dir test_results/cov_html


============================== 6 passed in 2.07s ==============================

All Tests Passed Successfully
=============================
```

## Package build

In the `VERSION` file update the `version` number and then run

```bash
python setup.py sdist bdist_wheel
```

## Package Deploy

to production

```bash
python -m twine upload dist/*VERSION*
```

or to test

```bash
python -m twine upload --repository testpypi dist/*VERSION*
```

Have binder build the new image: [binder](https://mybinder.org/v2/gh/MarcSkovMadsen/awesome-panel-extensions/master?filepath=examples%2Freference%2Fframeworks%2Fmaterial%2FMaterialIntSlider.ipynb)
