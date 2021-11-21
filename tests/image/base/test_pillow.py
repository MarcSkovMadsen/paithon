"""Test of the pillow module"""
import PIL
from panel_ai.image.base.pillow import ImageViewer, image_from_data_url, image_to_data_url


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

def test_load_image_from_datauri():
    # Given
    image=PIL.Image.new(mode="RGBA", size=(1920,1080), color="pink")
    uri = image_to_data_url(image)
    # When
    result = image_from_data_url(uri)
    # Then
    assert isinstance(result, PIL.Image.Image)
    assert image_to_data_url(result)==uri
