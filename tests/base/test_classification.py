"""Test of the classification module"""
from panel_ai.base.classification import ClassificationPlot
from panel_ai.image.image_classification import dummy_model


def test_classification_plot_constructor_with_no_arguments():
    """Can construct ClassificationPlot with no arguments"""
    ClassificationPlot()


def test_classification_plot_constructor_with_arguments():
    """Can construct ClassificationPlot with arguments"""
    _, _, output_json = dummy_model(None)
    ClassificationPlot(output_json=output_json)
