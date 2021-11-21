"""Tests of the DocStringViewer"""
from paithon.shared.pane.doc_string_viewer import DocStringViewer


def test_can_construct():
    """Can construct an instance"""
    some_parameterized = DocStringViewer()
    DocStringViewer(some_parameterized)
