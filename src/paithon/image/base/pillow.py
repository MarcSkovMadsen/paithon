"""Tools for working with pillow"""
import base64
import io
import urllib
from typing import Tuple

import numpy as np
import panel as pn
import param
import PIL
import requests


# Currently False. Should be changed to True later
def load_image_from_url(url: str, verify: bool = True) -> PIL.Image.Image:
    """Returns an image from from a url

    Args:
        url (str): A url
        verify (bool, optional): Whether or not to verify ssl certificate. Defaults to False.

    Returns:
        PIL.Image.Image: The PIL Image
    """
    return PIL.Image.open(requests.get(url, stream=True, verify=verify).raw)


def image_from_data_uri(data_url: str) -> PIL.Image.Image:
    """Returns an image from from a dataurl

    Args:
        url (str): A dataurl

    Returns:
        PIL.Image.Image: The PIL Image
    """
    return PIL.Image.open(urllib.request.urlopen(data_url).file)


def numpy_array_from_data_uri(data_uri: str, shape: Tuple[int, int]) -> np.ndarray:
    image = image_from_data_uri(data_uri)
    if image.mode == "RGBA":
        background = PIL.Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
    else:
        background = image
    background = background.resize(shape)
    return np.asarray(background)


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


def image_to_data_uri(img: PIL.Image.Image) -> str:
    """Returns a base64 encoded data uri for use as the src attribute of an img tag

    Args:
        img (PIL.Image.Image): The PIL Image to convert

    Returns:
        str: A base64 encoded data uri
    """
    img_format = img.format.lower()
    return f"data:image/{img_format};base64," + image_to_base64_string(img)


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
                self.data_url = image_to_data_uri(self.image)
            else:
                self.data_url = ""
