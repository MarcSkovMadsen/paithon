from base64 import b64decode
import panel as pn
import param
import PIL

from ...base.reactive import read_scripts
from ...base.component import get_theme
from ..base.pillow import image_from_data_url

class ImageInput(pn.reactive.ReactiveHTML):
    """The ImageInput can be used get an image from the user. Furthermore it enables

- Viewing the image in the input
- Setting an image from the server side
"""

    value = param.Parameter(constant=True, precedence=-1)
    filename = param.String(constant=True, doc="""
    The file name. For example 'image.png'.
    """)
    mime_type = param.String(constant=True, doc="""
    The mime type. For example 'image/png'.
    """)
    accept = param.ListSelector(default=["png", "jpg", "jpeg", "bmp", "gif"],objects=["png", "jpg", "jpeg", "bmp", "gif"],
        doc="""
    List of image file extensions (png, jpg, jpeg, gif, bmp etc.).
    """,
    )
    max_size_in_mega_bytes = param.Integer(10, doc="""
    Maximum file size in Mega Bytes.
    """)
    fit = param.Selector(default="contain", objects=["contain", "fill"], doc="""
    How to fit the image to the container: 'contain' or 'fill'.
    """)
    progress=param.Integer(constant=True, bounds=(0,100), doc="""
    The progress of the image file transfer.
    """)
    theme = param.Selector(
        default="default",
        objects=["default", "dark"],
        constant=True,
        doc="""
    The theme of the component. Either 'default' or 'dark'.""",
    )
    multiple = param.Boolean(default=False, constant=True, doc="""
    Whether or not to enable uploading multiple files. Currently only False is supported.
    """)
    # To be renamed to data_url later.
    # See https://github.com/holoviz/panel/issues/2937#issuecomment-974696364
    _url = param.Parameter(constant=True, doc="""
    Private parameter used to transfer the image.
    """)

    _template = """
<style>
.drop-region {
	background-color: inherit;
	border-radius: 4px;
    height: calc(100% - 4px);
	width: calc(100% - 4px);
    border: 2px dashed;
	text-align: center;
	cursor:pointer;
	transition:.3s;
    vertical-align: middle;
    white-space: nowrap;
}
.drop-region.default {border-color: #EAEAEA}
.drop-region.dark {border-color: #2E2E2E}
.drop-region.default:hover {box-shadow:0 0 25px rgba(0,0,0,0.1)}
.drop-region.dark:hover {box-shadow:0 0 25px rgba(0,0,0,0.3)}
.helper {
    display: inline-block;
    height: 100%;
    vertical-align: middle;
}
.drop-message{
    font-size: 1.5em;
}
</style>
<div id="dropRegion" class="drop-region ${theme}" title="Drag & Drop images or click to upload">
    <span class="helper"></span>
    <span id="drop_message" class="drop-message">
		<em>Drag & Drop</em> images or <em>click</em> to upload
	</span>
    <img id="imageRegion" style="height:100%;width:100%;object-fit:{{fit}};display:none;vertical-align:middle"/>
</div>

"""

    _scripts = read_scripts("image_input.js", __file__)


    def __init__(self, **params):
        params["theme"] = params.get("theme", get_theme())
        if "multiple" in params and params["multiple"]:
            raise ValueError("multiple=True is currently not supported")
        if "_url" in params:
            raise ValueError("Don't set the _url parameter directly. Use for example the set_value_from_data_url method.")
        super().__init__(**params)

    @param.depends("_url", watch=True)
    def _handle_url_change(self):
        # self.image=image_from_data_url(self._url)
        url = self._url
        if not url:
            self.value = None
            return

        index = url.find(",")
        if index<0:
            self.value = None
            return

        b64 = url[index+1:]
        with param.edit_constant(self):
            self.value=b64decode(b64)


    def set_value_from_data_url(self, data_url):
        with param.edit_constant(self):
            self._url=data_url

    def get_pil_image(self) -> 'PIL.Image.Image':
        return image_from_data_url(self._url)
