from panel_ai.shared.param import Param
import param

class MockClass(param.Parameterized):
    p2 = param.String()
    p1 = param.String()

def test_param():
    mock = MockClass()
    result = Param(mock)
    assert result._ordered_params == ["p1", "p2"]