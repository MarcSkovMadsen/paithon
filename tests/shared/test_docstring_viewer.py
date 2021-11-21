"""Tests of the DocStringViewer"""
from panel_ai.shared.pane.doc_string_viewer import DocStringViewer


def test_can_construct():
    """Can construct an instance"""
    some_parameterized = DocStringViewer()
    DocStringViewer(some_parameterized)
