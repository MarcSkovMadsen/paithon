from panel import Param as _Param

class Param(_Param):
    @property
    def _ordered_params(self):
        return sorted(super()._ordered_params)
