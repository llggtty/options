#!/usr/bin/venv python3.7
import numpy as np
import pandas as pd
from options.common.config import *
from options.core.bs_model import BlackScholesModel as bs, Option
pd.options.display.float_format = '{:,.3f}'.format
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 2000)

import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')


def generate_base_prices(p0: float, annual_return: float, volatility: float, trading_days: int) -> np.ndarray:
    """
    first generate a return series following normal distribution
    :param p0: price at time0
    :param annual_return: expected annual return
    :param volatility: expected annual volatility
    :param trading_days: int
    :return: series of daily price
    """

    sigma = volatility / math.sqrt(TRADING_DAYS)
    mu = annual_return / TRADING_DAYS
    # return from day 1
    ret = np.random.normal(mu, sigma, trading_days)
    prices = p0 * np.exp(np.cumsum(ret))
    # prices from day 0
    return np.insert(prices, [0], p0)


def generate_pricing_data(p0: float, annual_return: float, volatility: float, days_to_expiry: int) -> pd.DataFrame:
    """
    generate option pricing data based on configured pricing inputs
    :return: dataframe of base price, tte and the corresponding option price, delta
    """
    arr_base = generate_base_prices(p0, annual_return, volatility, days_to_expiry)
    # including day 0
    arr_tte = [(days_to_expiry + 1 - x) / (days_to_expiry + 1) for x in np.arange(0, days_to_expiry+1)]
    pricing_data = pd.DataFrame(data={'base_price': arr_base, 'tte': arr_tte})
    pricing_data['option_price'] = pricing_data.apply(
        lambda row: bs.value(Option.Call, row.tte, strike, row.base_price, annual_volatility, r), axis=1)
    pricing_data['delta'] = pricing_data.apply(
        lambda row: bs.delta(Option.Call, row.tte, strike, row.base_price, annual_volatility, r), axis=1)
    return pricing_data


def portfolio_pnl(pricing_data: pd.DataFrame) -> float:
    """
    :param pricing_data: dataframe of base price, tte and the corresponding option price, delta
    :return: dataframe of # of stocks for hedge and the pnl.
    """
    last_row = len(pricing_data) - 1
    # hedge can only be integer
    pricing_data['hedge'] = -(pricing_data['delta'] * contract_multiplier).astype(int)
    pricing_data['hedge_volume'] = pricing_data['hedge'].shift(1) - pricing_data['hedge']
    # the first trade is the hedge amount
    pricing_data.loc[0, 'hedge_volume'] = pricing_data.loc[0, 'hedge']

    pricing_data['hedge_pnl'] = pricing_data['hedge_volume'] * (pricing_data.loc[last_row, 'base_price']-pricing_data['base_price'])
    option_pnl = (pricing_data.loc[last_row, 'option_price'] - pricing_data.loc[0, 'option_price']) * contract_multiplier
    final_pnl = pricing_data['hedge_pnl'].sum() + option_pnl
    return final_pnl



def realised_volatility(p: pd.Series) ->float:
    """
    :param p: price series
    :return: annualised realised volatility
    """
    t = len(p)
    def gamma_pnl(ds, gamma):
        returns = ds / ds.iloc[0]
        d = returns.diff().iloc[1:]
        d = d.apply(lambda v: gamma * 0.5 * v**2)
        return d.cumsum()

    def pnl_to_vol(pnl, gamma, t):
        return math.sqrt(2*pnl/(gamma * t/TRADING_DAYS))


def analytical_realised_volatility(p: pd.Series) ->float:
    """
    :param p: price series
    :return: annualised realised volatility
    """
    r = np.log(p.shift(1)/p).dropna()
    return math.sqrt(sum(r**2) * len(r)/TRADING_DAYS)