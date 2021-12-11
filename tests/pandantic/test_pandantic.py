from datetime import datetime
from typing import Any, List, Optional

import param
from param.parameterized import Parameterized
import pydantic
import pytest
from paithon.pandantic import (Pydantic,
                               _get_parameter_type_from_pydantic_field,
                               _get_python_type_from_parameter,
                               param_to_pydantic_class,
                               pydantic_to_param_class, parameterize)
from pydantic import BaseModel

@pytest.fixture
def user():
    class User(BaseModel):
        id: int
        name: str = "John Doe"
        signup_ts: datetime
        friends: List[int]

    external_data = {
        "id": "123",
        "signup_ts": "2019-06-01 12:22",
        "friends": [1, 2, "3"],
    }
    return User(**external_data)

@pytest.mark.parametrize(
    ["parameter", "python_type"],
    [
        (param.String(default="test"), str),
        (param.String(default="test", allow_None=True), Optional[str]),
    ],
)
def test_get_python_type_from_parameter(parameter, python_type):
    class MyClass(param.Parameterized):
        value = parameter

    assert _get_python_type_from_parameter(MyClass.param.value) == python_type


@pytest.mark.parametrize(
    ["parameter"],
    [
        (param.String(default="test"),),
        (param.String(default="test", allow_None=True),),
    ],
)
def test_param_to_pydantic_class(parameter):
    class MyClass(param.Parameterized):
        value = parameter

    result = param_to_pydantic_class(MyClass)
    assert result.__name__ == MyClass.__name__
    assert result().name == MyClass.__name__
    assert result().value == MyClass.param.value.default


def test_can_handle_allow_None_False():
    class ParamClass(param.Parameterized):
        value = param.String(default="test", allow_None=False)

    # When/ Then
    pydantic_class = param_to_pydantic_class(ParamClass)
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        pydantic_class(value=None)

    # When/ Then
    param_class = pydantic_to_param_class(pydantic_class)
    assert not param_class.param.value.allow_None
    with pytest.raises(ValueError):
        param_class(value=None)


def test_can_handle_allow_None_True():
    class MyClass(param.Parameterized):
        value = param.String(default="test", allow_None=True)

    MyClass(value=None)
    result = param_to_pydantic_class(MyClass)
    result(value=None)
    result = pydantic_to_param_class(result)
    result(value=None)


def test_can_handle_default():
    class MyClass(param.Parameterized):
        value = param.String(default="test")

    pydantic_class = param_to_pydantic_class(MyClass)
    assert pydantic_class.__fields__["value"].default == "test"
    assert pydantic_class().value == "test"
    param_class = pydantic_to_param_class(pydantic_class)
    assert param_class.param.value.default == "test"
    assert param_class().value == "test"


def test_do_allow_none():
    class MyClass(param.Parameterized):
        value = param.String(default="test", allow_None=True)

    param_instance = MyClass(value=None)
    assert not param_instance.value
    pydantic_class = param_to_pydantic_class(MyClass)
    pydantic_instance = pydantic_class(value=None)
    assert not pydantic_instance.value


def test_python_type_to_param():
    class MyClass(pydantic.BaseModel):
        name: Optional[str] = "John Doe"

    parameter = _get_parameter_type_from_pydantic_field(MyClass.__fields__["name"])
    assert parameter == param.String

def test_python_type_to_param_list():
    class MyClass(pydantic.BaseModel):
        friends: List[int]

    parameter = _get_parameter_type_from_pydantic_field(MyClass.__fields__["friends"])
    assert parameter == param.List


def test_list_of_int():
    class MyClass(param.Parameterized):
        value = param.List(item_type=int)

    pydantic_class = param_to_pydantic_class(MyClass)
    assert pydantic_class.__fields__["value"].outer_type_ == List[int]

    param_class = pydantic_to_param_class(pydantic_class)
    assert isinstance(param_class.param.value, param.List)
    assert param_class.param.value.item_type==int


def test_pydantic_to_param():
    parameter = param.String(default="John Doe")

    class MyClass(param.Parameterized):
        value = parameter

    py_value = param_to_pydantic_class(MyClass)
    param_value = pydantic_to_param_class(py_value)

    original = MyClass().param.values()
    original.pop("name")

    new = param_value().param.values()
    new.pop("name")
    assert original == new


def test_pydantic(user):
    param_user = Pydantic(object=user, sync_from_object=True)
    assert isinstance(param_user, param.Parameterized)
    assert param_user.object==user
    assert param_user.id==user.id
    assert param_user.signup_ts==user.signup_ts
    assert param_user.friends==user.friends

    # When
    param_user.id=1234
    assert user.id == param_user.id
    param_user.name = "Marc Skov Madsen"
    assert user.name == param_user.name
    param_user.signup_ts = datetime(2019,6,1,13,23)
    assert user.signup_ts == param_user.signup_ts
    param_user.friends = [1,2,3,4]
    assert user.friends == param_user.friends

    # When
    user.id=1234567
    assert param_user.id == user.id
    user.name = "Philipp Rudiger"
    assert param_user.name == user.name
    user.signup_ts = datetime(2019,6,1,13,24)
    assert param_user.signup_ts == user.signup_ts
    user.friends = [1,2,3,4,5]
    assert param_user.friends == user.friends

def test_pydantic_can_exclude_fields():
    class User(BaseModel):
        field: Any

    user=User(field="some value")
    param_user = Pydantic(object=user, exclude=["field"])

    assert not hasattr(param_user, "field")
def test_can_parameterize(user):
    param_user = parameterize(object=user)
    isinstance(param_user, Parameterized)
    assert param_user == user.parameterized

def test_can_parameterize_to_custom_field(user):
    param_user = parameterize(object=user, field="parameterized2")
    isinstance(user.parameterized2, Parameterized)
    assert param_user==user.parameterized2

def test_can_parameterize_twice(user):
    first = parameterize(object=user)
    second = parameterize(object=user)
    assert first==second


if __name__.startswith("bokeh"):
    import panel as pn
    pn.extension(sizing_mode="stretch_width")
    class User(BaseModel):
        id: int
        name: str = "John Doe"
        signup_ts: datetime
        friends: List[int]

    external_data = {
        "id": "123",
        "signup_ts": "2019-06-01 12:22",
        "friends": [1, 2, "3"],
    }
    user = User(**external_data)
    parameterize(object=user)
    @pn.depends(id=user.parameterized.param.id, watch=True)
    def write(id):
        print(id)

    pn.Param(user.parameterized, parameters=["name", "id"]).servable()
