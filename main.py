#!/usr/bin/venv python3.7
import pandas as pd
from options.core.bs_model import Option
from options.utils.dgp import generate_base_prices, generate_pricing_data, realised_volatility, portfolio_pnl
from options.core.instruments import Instrument, implied_forward
from options.common.config import *
import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', filename='main.log')
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


pd.options.display.float_format = '{:,.3f}'.format
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 2000)


# question 1



# question 2
pricing_data = generate_pricing_data(initial_price, annual_return, annual_volatility, days_to_expiry)
rvol = realised_volatility(pricing_data['base_price'])
# if realised vol > implied vol, portfolio pnl > 0.
pnl = portfolio_pnl(pricing_data)

print(pnl, rvol, annual_volatility)


# question 3

k1 = 100
k2 = 120
c1 = Instrument(Option.Call, tte, k1, initial_price, annual_volatility, r)
c2 = Instrument(Option.Call, tte, k2, initial_price, annual_volatility, r)
p1 = Instrument(Option.Put, tte, k1, initial_price, annual_volatility, r)
p2 = Instrument(Option.Put, tte, k2, initial_price, annual_volatility, r)

for i in [c1, c2, p1, p2]:
    i.price = i.calculate_price()

expected_forward = initial_price * math.exp(r * tte)

print(f"forward : {expected_forward}, implied forward from options {implied_forward(p1, c1, p2, c2)}")


if __name__ == '__main__':
    pricing_data = generate_pricing_data(initial_price, annual_return, annual_volatility, days_to_expiry)
    rvol = realised_volatility(pricing_data['base_price'])
    # if realised vol > implied vol, portfolio pnl > 0.
    pnl = portfolio_pnl(pricing_data)

    print(pnl, rvol, annual_volatility)
