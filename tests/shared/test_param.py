"""Tests of the Panel param extensions"""
import param

from paithon.shared.param import SortedParam


class _MockClass(param.Parameterized):
    p2 = param.String()
    p1 = param.String()


def test_param():
    """Test that the widgets of SortedParam are sorted alphabetically."""
    mock = _MockClass()
    result = SortedParam(mock)
    assert result._ordered_params == ["p1", "p2"]  # pylint: disable=protected-access
