from datetime import datetime, date
from typing import Any, Container, Dict, List, Optional, Type, Union

import param
from param.parameterized import Parameterized
import pydantic
from pydantic import BaseConfig, BaseModel, create_model

try:
    import numpy as np

    DATE_TYPE = Union[datetime, date, np.datetime64]
except:
    DATE_TYPE = Union[datetime, date]

PARAM_TO_PYTHON_TYPE: Dict[param.Parameter, Type] = {
    param.String: str,
    param.Integer: int,
    param.Number: float,
    param.Date: DATE_TYPE,
    param.List: List,
    param.Parameter: Any,
}
PYTHON_TYPE_TO_PARAM = {
    str: param.String,
    int: param.Integer,
    float: param.Number,
    DATE_TYPE: param.Date,
    datetime: param.Date,
    date: param.Date,
    List: param.List,
    list: param.List,
    Any: param.Parameter,
}

def _get_python_type_from_parameter(parameter: param.Parameter):
    if isinstance(parameter, param.List) and parameter.item_type:
        python_type: Type = List[parameter.item_type]
    else:
        python_type = PARAM_TO_PYTHON_TYPE[parameter.__class__]

    if parameter.allow_None:
        python_type = Union[python_type, None]

    return python_type


def _get_parameter_type_from_python_type(type_: Type) -> Type[param.Parameter]:
    return PYTHON_TYPE_TO_PARAM[type_]


def _get_parameter_type_from_pydantic_field(
    field: pydantic.fields.ModelField,
) -> Type[param.Parameter]:
    try:
        return _get_parameter_type_from_python_type(field.outer_type_.__origin__)
    except:
        return _get_parameter_type_from_python_type(field.type_)


def param_to_pydantic_class(
    parameterized: Type[param.Parameterized],
    *,
    config: Type = BaseConfig,
    exclude: Container[str] = ["param"]
) -> Type[BaseModel]:
    fields = {}
    parameters = [
        parameterized.param[key]
        for key in parameterized.param
        if not parameterized.param[key].name in exclude
    ]
    for parameter in parameters:
        python_type = _get_python_type_from_parameter(parameter)
        fields[parameter.name] = (python_type, parameter.default)
    pydantic_model = create_model(parameterized.__name__, __config__=config, **fields)  # type: ignore
    return pydantic_model

def _add_pydantic_fields(value: BaseModel, parameterized: param.Parameterized, exclude: Container[str] = []):
    for name, field in value.__fields__.items():
        if name in exclude:
            continue
        parameter_type = _get_parameter_type_from_pydantic_field(field)
        if parameter_type==param.List:
            parameter = parameter_type(default=field.default, allow_None=field.allow_none, item_type=field.type_)
        else:
            parameter = parameter_type(default=field.default, allow_None=field.allow_none)
        parameterized.param.add_parameter(name, parameter)
    return parameterized

def pydantic_to_param_class(value) -> param.Parameterized:
    parameterized: param.Parameterized = type(value.__name__, (param.Parameterized,), {})

    return _add_pydantic_fields(value, parameterized)


class Pydantic(param.Parameterized):
    object = param.ClassSelector(class_=BaseModel)

    def __init__(self, object: BaseModel, sync_to_object=True, sync_from_object=False, exclude=[]):
        super().__init__(object=object)
        _add_pydantic_fields(object, self, exclude=exclude)

        def update_self(values_):
            values_ = {key: value for key, value in values_.items() if not key in exclude}
            self.param.update(**values_)
        update_self(object.dict())

        if sync_to_object:
            self._updating = False
            parameter_names = [key for key in self.param]
            self.param.watch(self.handle_change, parameter_names=parameter_names)

        if sync_from_object:
            object.Config.validate_assignment=True
            def watcher(cls, values):
                update_self(values)
                return values

            object.__post_root_validators__.append(
                (False, watcher)
            )

    def handle_change(self, *events):
        if self._updating:
            return

        self._updating=True
        for ev in events:
            setattr(self.object, ev.name, ev.new)
        self._updating=False

def parameterize(object: BaseModel, sync_to_object=True, sync_from_object=False, field="parameterized"):
    if hasattr(object, field):
        if isinstance(getattr(object, field), Pydantic):
            return getattr(object, field)
        else:
            raise ValueError("The field {field} is already in use. Please use another one")
    parameterized = Pydantic(object=object, sync_to_object=sync_to_object, sync_from_object=sync_from_object)
    if field:
        object.__private_attributes__[field]=parameterized
        object.__setattr__(field, parameterized)

    object.__private_attributes__["__parameterized__"]=True
    object.__setattr__("__parameterized__", True)
    return parameterized
