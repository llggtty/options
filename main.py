#!/usr/bin/venv python3.7
import math
import pandas as pd
from options.core.bs_model import Option, BlackScholesModel as bs
from options.utils.dgp import generate_base_prices, generate_pricing_data, annual_realised_volatility, portfolio_pnl
from options.core.instruments import Instrument, implied_forward
from options.common.config import initial_price, annual_return, annual_volatility, days_to_expiry, tte, strike, rate, k1, k2
import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')

pd.options.display.float_format = '{:,.3f}'.format
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
desired_width = 320
pd.set_option('display.width', desired_width)


# set up logger
def set_up_logger():
    global log
    fh = logging.FileHandler('main.log', mode='w+')
    sh = logging.StreamHandler()
    logging.getLogger().addHandler(fh)
    logging.getLogger().addHandler(sh)
    log = logging.getLogger(__file__)
    log.setLevel(logging.INFO)


# question 1
def question_1():
    base_price = generate_base_prices(initial_price, annual_return, annual_volatility, days_to_expiry)
    log.info(f"A series of prices follows log normal distribution: \n {base_price}")


# question 2
def question_2():
    kind = Option.Call

    pricing_data = generate_pricing_data(initial_price, annual_return, annual_volatility, days_to_expiry, strike, r=0)
    # delta hedge based on our expected vol
    log.info(f"Use implied vol for calculating delta to hedge: ")
    pnl, hedge = portfolio_pnl(pricing_data, rounding=False)
    rvol = annual_realised_volatility(pricing_data['base_price'])
    log.info(f"The daily hedge portfolio final pnl : {pnl:,.4f}, realised vol {rvol:.4f}, "
             f"implied vol of the option {annual_volatility:4f}.")

    # numeric delta
    log.info(f"Use numeric delta to hedge: ")
    # let's start with only one day left, to be exactly pnl flat, the hedge volume V0 = -(P1 - P0)/ (S1-S0) * 100.
    numeric_delta = (pricing_data.shift(1)['option_price'] - pricing_data['option_price'])/(pricing_data.shift(1)['base_price'] - pricing_data['base_price'])
    pricing_data.loc[0:days_to_expiry-1, 'delta'] = numeric_delta.dropna().reset_index(drop=True)

    pnl, hedge = portfolio_pnl(pricing_data, rounding=False)
    log.info(f"The daily hedge portfolio final pnl : {pnl:,.4f}.")

    # use the realised return to calculate realised vol
    log.info(f"Use delta calculated by realised vol to hedge: ")

    # compare with numeric delta
    pricing_data['delta'] = pricing_data.apply(lambda row: bs.delta(kind, row.tte, strike, row.base_price, rvol, r=0), axis=1)
    pnl, hedge = portfolio_pnl(pricing_data, rounding=False)
    log.info(f"The daily hedge portfolio final pnl : {pnl:,.4f}.")


# question 3
def question_3():

    c1 = Instrument(Option.Call, tte, k1, initial_price, annual_volatility, rate)
    c2 = Instrument(Option.Call, tte, k2, initial_price, annual_volatility, rate)
    p1 = Instrument(Option.Put, tte, k1, initial_price, annual_volatility, rate)
    p2 = Instrument(Option.Put, tte, k2, initial_price, annual_volatility, rate)

    for i in [c1, c2, p1, p2]:
        i.price = i.calculate_price()

    expected_forward = initial_price * math.exp(rate * tte)

    log.info(f"forward : {expected_forward:4f}, implied forward from options {implied_forward(p1, c1, p2, c2):.4f}")


if __name__ == '__main__':
    set_up_logger()
    question_1()
    question_2()
    question_3()
