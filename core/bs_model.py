#!/usr/bin/venv python3.7
import math
from enum import Enum
from options.utils.stats import norm_cdf, norm_pdf


class Option(Enum):
    Put = 1
    Call = 2

    def __str__(self):
        return self.name


class BlackScholesModel(object):

    @classmethod
    def value(cls, kind: Option, tte: float, strike: int, spot: float, volatility: float, r: float) -> float:
        if kind not in [Option.Put, Option.Call]:
            raise NotImplementedError
        if tte == 0:
            if kind == Option.Call:
                return max(spot - strike, 0)
            else:
                return max(strike - spot, 0)
        elif tte > 0:
            discount_factor = math.exp(-r * tte)
            d1, d2 = cls.d1_d2(tte, strike, spot, volatility, r)
            if kind == Option.Call:
                return max(norm_cdf(d1) * spot - norm_cdf(d2) * strike * discount_factor, 0)
            else:
                return max(norm_cdf(-d2) * strike * discount_factor - norm_cdf(-d1) * spot, 0)
        else:
            raise ValueError

    @classmethod
    def d1_d2(cls, tte: float, strike: int, spot: float, volatility: float, r: float) -> tuple[float, float]:
        d1 = math.log(spot/strike + (r+0.5*volatility**2) * tte)/(volatility*math.sqrt(tte))
        d2 = d1 - volatility*math.sqrt(tte)
        return d1, d2

    @classmethod
    def delta(cls, kind: Option, tte: float, strike: int, spot: float, volatility: float, r: float):
        if kind not in [Option.Put, Option.Call]:
            raise NotImplementedError

        d1, _ = cls.d1_d2(tte, strike, spot, volatility, r)

        if kind == Option.Call:
            return norm_cdf(d1)
        else:
            return norm_cdf(d1) - 1

    @classmethod
    def gamma(cls, tte: float, strike: int, spot: float, volatility: float, r: float):
        d1, _ = cls.d1_d2(tte, strike, spot, volatility, r)
        return norm_pdf(d1) / (spot * volatility * math.sqrt(tte))


if __name__ == '__main__':
    bs = BlackScholesModel
    bs.value(Option.Call, 1, 100, 100, 0.3, 0.05)