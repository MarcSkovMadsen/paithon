"""Tools for working with pillow"""
import base64
import io

import panel as pn
import param
import PIL
import requests


def load_image_from_url(url: str, verify: bool = False) -> PIL.Image.Image:
    """Returns an image from from a url

    Args:
        url (str): A url
        verify (bool, optional): Whether or not to verify ssl certificate. Defaults to False.

    Returns:
        PIL.Image.Image: The PIL Image
    """
    return PIL.Image.open(requests.get(url, stream=True, verify=verify).raw)


def image_to_base64_string(img: PIL.Image.Image) -> str:
    """Returns a base64 encoded string

    Args:
        img (PIL.Image.Image): The PIL Image to convert

    Returns:
        str: a base64 encoded string
    """
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def image_to_data_url(img: PIL.Image.Image) -> str:
    """Returns a base64 encoded data url for use as the src attribute of an img tag

    Args:
        img (PIL.Image.Image): The PIL Image to convert

    Returns:
        str: A base64 encoded data url
    """
    img_format = img.format.lower()
    return f"data:image/{img_format};base64," + image_to_base64_string(img)


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


class ImageViewer(pn.reactive.ReactiveHTML):
    """An ImageViewer for PIL Images"""

    image = param.ClassSelector(
        class_=PIL.Image.Image,
        precedence=-1,
        doc="""
    A PIL Image""",
    )
    data_url = param.String(
        constant=True,
        doc="""
    Used to transfer the image to the client and view it""",
    )

    _template = (
        """<div id="component" style="height:100%;width:100%">"""
        """<img id="image" src="${data_url}" """
        """style="height:100%;display:block;margin-left:auto;margin-right:auto;"></img>"""
        """</div>"""
    )

    def __init__(self, image: PIL.Image.Image = None, height=400, **params):
        super().__init__(image=image, height=height, **params)
        self._update_data_url()

    @param.depends("image", watch=True)
    def _update_data_url(self):
        with param.edit_constant(self):
            if self.image:
                self.data_url = image_to_data_url(self.image)
            else:
                self.data_url = ""
