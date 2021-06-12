#!/usr/bin/venv python3.7
import numpy as np
import math
from options.common.config import *


def data_generating_process(p0: float, mu: float, volatility: float, trading_days:int) -> np.ndarray:
    """
    first generate a return series following normal distribution
    :param p0: price at time0
    :param mu: expected annual return in percentage
    :param volatility: expected annual volatility in percentage
    :param trading_days: int
    :return: series of daily price
    """

    sigma = 0.01 * volatility / math.sqrt(TRADING_DAYS)
    mu = 0.01 * mu / TRADING_DAYS
    ret = np.random.normal(mu, sigma, trading_days)
    prices = p0 * np.exp(np.cumsum(ret))

    return prices
