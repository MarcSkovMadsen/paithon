"""Provides the IMAGE_EXAMPLES list of ImageExamples"""
import param
import PIL

from .base.pillow import image_to_data_uri, load_image_from_url


class ImageExample(param.Parameterized):
    """A model of an ImageExample"""

    url = param.String(constant=True)

    def __init__(self, **params):
        super().__init__(**params)

        self._image = None

    @property
    def image(self) -> PIL.Image.Image:
        """Return the PIL Image of the example

        Returns:
            PIL.Image.Image: A PIL Image
        """
        if not self._image and self.url:
            self._image = load_image_from_url(self.url)
        return self._image

    @property
    def data_uri(self) -> str:
        """Returns a data_uri from the pillow image

        Returns:
            String: a data_uri
        """
        return image_to_data_uri(self.image)


IMAGE_EXAMPLES = [
    ImageExample(
        url="https://huggingface.co/datasets/mishig/sample_images/resolve/main/tiger.jpg",
        name="Tiger",
    ),
    ImageExample(
        url="https://huggingface.co/datasets/mishig/sample_images/resolve/main/teapot.jpg",
        name="Teapot",
    ),
    ImageExample(
        url="https://huggingface.co/datasets/mishig/sample_images/resolve/main/palace.jpg",
        name="Palace",
    ),
]
