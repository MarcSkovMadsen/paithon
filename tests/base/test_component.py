"""Test of the component utility functions"""
import panel as pn

from panel_ai.base.component import get_theme


class MockState:  # pylint: disable=too-few-public-methods
    """Mock State to replace pn.state instance"""

    def __init__(self, session_args):
        self.session_args = session_args


def test_get_theme_none(mocker):
    """If no query args given then the default theme should be returned"""
    mocker.patch.object(pn, "state", MockState({}))
    assert get_theme() == "default"


def test_get_theme_default(mocker):
    """If theme='default' in query args then the default theme should be returned"""
    mocker.patch.object(pn, "state", MockState({"theme": [b"default"]}))
    assert get_theme() == "default"


def test_get_theme_dark(mocker):
    """If theme='dark' in query args then the dark theme should be returned"""
    mocker.patch.object(pn, "state", MockState({"theme": [b"dark"]}))
    assert get_theme() == "dark"


def test_get_theme_other(mocker):  # pylint: disable=missing-function-docstring
    """If theme query arg different from 'default' or 'dark' then the 'default' theme should be
    returned"""
    mocker.patch.object(pn, "state", MockState({"theme": [b"other"]}))
    assert get_theme() == "default"
