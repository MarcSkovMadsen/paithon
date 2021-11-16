import panel as pn
import param
import PIL


class ImageViewer(pn.reactive.ReactiveHTML):
    data_url = param.String(default="test_string", constant=True)

    _template = """<img id="value" src="" style="height:100%;width:100%">${data_url}</img>"""

    @property
    def image(self) -> PIL.Image.Image:
        return self._image

    @image.setter
    def image(self, value: PIL.Image.Image):
        self._image = value

    def __init__(self, image: PIL.Image.Image, params):
        super().__init__(**params)
        self.image = image


if __name__.startswith("bokeh"):
    image = PIL.Image.new("RGBA", size=(50, 50), color=(155, 0, 0))
    image.format = "PNG"
    ImageViewer(image=image).servable()
