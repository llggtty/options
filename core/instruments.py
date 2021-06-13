#!/usr/bin/venv python3.7
import math
from typing import Optional
from options.core.bs_model import Option, BlackScholesModel as bs
import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', filename='main.log')
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


class Instrument(object):
    def __init__(self, kind: Option, tte: float, strike: int, base_price: Optional[float] = None,
                 volatility: Optional[float] = None, r: Optional[float] = None, price: Optional[float] = None):
        self.kind = kind
        self.tte = tte
        self.strike = strike
        self.base_price = base_price
        self.volatility = volatility
        self.r = r
        self.price = price

    def calculate_price(self):
        if any([self.kind, self.tte, self.strike, self.base_price, self.volatility, self.r]) is None:
            ValueError(f"Need kind, tte, strike, base price, implied vol and rate as inputs.")
        else:
            return bs.value(self.kind, self.tte, self.strike, self.base_price, self.volatility, self.r)


def implied_discount_factor(p1: Instrument, c1: Instrument, p2: Instrument, c2: Instrument) -> float:
    """
    c1-p1 - (c2-p2) = (K2-K1)exp(-rt)
    :param p1: put of strike 1
    :param c1: call of strike 1
    :param p2: put of strike 2
    :param c2: call of strike 2
    :return: implied discount factor exp(-rt)
    """
    return (c1.price - p1.price - c2.price + p2.price)/ (c2.strike - c1.strike)


def implied_forward(p1: Instrument, c1: Instrument, p2: Instrument, c2: Instrument) -> float:
    """
    c1 - p1 = S - K1 exp(-rt)
    :param p1: put of strike 1
    :param c1: call of strike 1
    :param p2: put of strike 2
    :param c2: call of strike 2
    :return: implied forward
    """
    discount_factor = implied_discount_factor(p1, c1, p2, c2)
    spot = c1.price - p1.price + c1.strike * discount_factor
    return spot / discount_factor
