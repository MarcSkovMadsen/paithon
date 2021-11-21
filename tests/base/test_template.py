"""Test of the template module"""
from paithon.base.template import fastlisttemplate


def test_fastlisttemplate_constructor():
    """Can construct the FastListTemplate"""
    fastlisttemplate(title="Test App")
