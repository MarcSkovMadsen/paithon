"""The Model is wraps a function as a ParameterizedFunction
which makes it interactive and easier to interface.
"""
from typing import Dict, Optional

import param
from param import ParamOverrides


class Model(param.ParameterizedFunction):
    _non_function_parameters = ["name"]

    _function: Optional[staticmethod] = None

    @property
    def _function_parameters(self):
        return [
            parameter for parameter in self.param if not parameter in self._non_function_parameters
        ]

    def __call__(self, *args, **params):
        params = self._to_params(*args, **params)
        return self._function(**params)

    def _to_params(self, *args, **params):
        args_params = {}
        for index, value in enumerate(args):
            key = self._function_parameters[index]
            args_params[key] = value
        params = {**args_params, **params}

        p = ParamOverrides(self, params)
        return {key: p[key] for key in self._function_parameters}

    @property
    def kwargs(self) -> Dict:
        """Returns the model parameters and current values

        Returns:
            Dict: A dictionary of model parameters and their values
        """
        return self._to_params()