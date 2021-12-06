"""Provides different types of Pipes: PanelPipe, ParameterizedPipe, ..."""
import panel as pn
import param

NONE_OR_EMPTY_HACK = "&nbsp;"


class BasePipe(param.Parameterized):
    """An abstract base class for Piping an object to an output."""

    object = param.Parameter()
    output = param.Parameter(constant=True)

    loading = param.Boolean()

    def _handle_object_changed(self, *_):
        raise NotImplementedError()

    def _handle_loading_changed(self, *_):
        raise NotImplementedError()

    def __init__(self, **params):
        super().__init__(**params)

        self.param.watch(self._handle_loading_changed, "loading")
        self.param.watch(self._handle_object_changed, "object")

        self._handle_loading_changed()
        self._handle_object_changed()


class PanelPipe(BasePipe):
    """Pipes the object to an output determined by pn.panel"""

    transform = param.Callable(default=lambda x: x)

    def __init__(self, object=None, **params):
        super().__init__(object=object, **params)

        with param.edit_constant(self):
            self.output = pn.panel(self._itransform)

    @param.depends("object")
    def _itransform(self):
        value = self.object
        if self.object is None or self.object == "":
            # Hack: C.f. https://github.com/holoviz/panel/issues/2977
            value = NONE_OR_EMPTY_HACK
        return self.transform(value)

    def _handle_object_changed(self, *_):
        pass

    def _handle_loading_changed(self, *_):
        if self.output:
            self.output._pane.loading = self.loading


class ParameterizedPipe(BasePipe):
    output = param.ClassSelector(class_=param.Parameterized, constant=True)
    parameter = param.String(constant=True)

    def _handle_object_changed(self, *_):
        if self.object is None:
            value = self.output.param[self.parameter].default
        else:
            value = self.object
        setattr(self.output, self.parameter, value)

    def _handle_loading_changed(self, *_):
        self.output.loading = self.loading


def create_pipe(output, object=None):
    if type(output) is param.parameterized.ParameterizedMetaclass:
        return create_pipe(output(), object=object)

    if isinstance(output, param.Parameter) and not isinstance(output.owner, param.Parameterized):
        return create_pipe(output.owner().param[output.name], object=object)

    if isinstance(output, param.Parameterized):
        if "object" in output.param:
            return ParameterizedPipe(output=output, object=object, parameter="object")
        if "value" in output.param:
            return ParameterizedPipe(output=output, object=object, parameter="value")
        raise ValueError(
            f"""The output {output} is a Parameterized without an `object` or `value`
        parameter. Cannot determine parameter to pipe to. Provide as a parameter instead."""
        )

    if isinstance(output, param.Parameter):
        return ParameterizedPipe(output=output.owner, object=object, parameter=output.name)

    if not output:
        return PanelPipe(object=object)

    if callable(output):
        return PanelPipe(object=object, transform=output)

    raise ValueError(f"""Output {output} is not a valid output.""")
