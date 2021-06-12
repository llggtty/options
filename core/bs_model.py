import numpy as np
import math
from enum import Enum
from options.common.config import *

class Option(Enum):
    Put = 1
    Call = 2

    def __str__(self):
        return self.name


class BlackScholesModel(object):

    @classmethod
    def value(cls, kind: Option, tte: float, strike: int, spot: float, sigma: float, r: float) -> float:
        if kind not in [Option.Put, Option.Call]:
            raise NotImplementedError
        if tte == 0:
            if kind == Option.Call:
                return max(spot - strike, 0)
            else:
                return max(strike - spot, 0)
        elif tte > 0:
            discount_factor = math.exp(-r * tte)
            d1, d2 = cls.d1_d2(tte, strike, spot, sigma, r)

        else:
            raise ValueError

    @classmethod
    def d1_d2(cls, tte: float, strike: int, spot: float, sigma: float, r: float) -> tuple[float, float]:
        d1 = math.log(spot/strike) + (r+0.5*sigma**2) * tte/(sigma*math.sqrt(tte))
        d2 = d1 - sigma*math.sqrt(tte)
        return d1, d2

