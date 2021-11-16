"""Shared test functionality for images"""
import pytest
from PIL import Image

from tests.data import DATA_PATH


def get_image() -> Image.Image:
    """Returns a test image"""
    return Image.open(DATA_PATH / "coins.png")


@pytest.fixture
def image() -> Image.Image:
    """Return a test image"""
    return get_image()
