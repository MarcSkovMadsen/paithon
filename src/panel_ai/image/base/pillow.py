"""Tools for working with pillow"""
import base64
import io

import panel as pn
import param
import PIL


def image_to_base64_string(img: PIL.Image.Image) -> str:
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def image_to_data_url(img: PIL.Image.Image) -> str:
    img_format = img.format.lower()
    return f"data:image/{img_format};base64," + image_to_base64_string(img)


class ImageViewer(pn.reactive.ReactiveHTML):
    image = param.ClassSelector(class_=PIL.Image.Image, precedence=-1)
    data_url = param.String(constant=True)

    _template = """<div id="component" style="height:100%;width:100%"><img id="image" src="${data_url}" style="height:100%;display:block;margin-left:auto;margin-right:auto;"></img></div>"""

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
