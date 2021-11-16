"""Test of the pillow module"""
from panel_ai.image.base.pillow import ImageViewer


def test_image_viewer_construction_without_image():
    """Can construct ImageViewer with no arguments"""
    viewer = ImageViewer()
    assert not viewer.image
    assert viewer.data_url == ""


def test_image_viewer_construction_with_image(image):
    """Can construct ImageViewer with an image as argument"""
    viewer = ImageViewer(image)
    assert viewer.image == image
    assert viewer.data_url.startswith("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA")


def test_image_viewer_change_image(image):
    """Can change the image"""
    viewer = ImageViewer()
    viewer.image = image
    assert viewer.image == image
    assert viewer.data_url.startswith("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA")
