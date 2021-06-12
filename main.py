#!/usr/bin/venv python3.7
from options.utils.dgp import *
from options.common.config import *
pd.options.display.float_format = '{:,.3f}'.format
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 2000)


if __name__ == '__main__':
    pricing_data = generate_pricing_data(initial_price, annual_return, annual_volatility, days_to_expiry)
    rvol = realised_volatility(pricing_data['base_price'])
    # if realised vol > implied vol, portfolio pnl > 0.
    pnl = portfolio_pnl(pricing_data)

    print(pnl, rvol, annual_volatility)
