"""Improved version of Panels Param"""
from panel import Param as _Param


class SortedParam(_Param):  # pylint: disable=abstract-method
    """A version Param that sorts the widgets alphabetically."""

    @property
    def _ordered_params(self):
        return sorted(super()._ordered_params)
