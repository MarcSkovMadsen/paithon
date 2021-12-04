"""Test of the classification module"""
from paithon.image.image_classification import dummy_model
from paithon.shared.pane.label import Label


def test_classification_plot_constructor_with_no_arguments():
    """Can construct ClassificationPlot with no arguments"""
    Label()


def test_classification_plot_constructor_with_arguments():
    """Can construct ClassificationPlot with arguments"""
    _, _, output_json = dummy_model(None)
    Label(object=output_json)
